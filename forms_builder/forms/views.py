from __future__ import unicode_literals

import json
import datetime

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.template import RequestContext
from django.utils.http import urlquote
from django.views.generic.base import TemplateView
from django.db.models import Q
from email_extras.utils import send_mail_template

from forms_builder.forms.forms import FormForForm
from forms_builder.forms.models import Form, FormsList
from forms_builder.forms.settings import EMAIL_FAIL_SILENTLY
from forms_builder.forms.signals import form_invalid, form_valid
from forms_builder.forms.utils import split_choices

from terms.views import update_user as terms_update_user


class FormDetail(TemplateView):

    template_name = "forms/form_detail.html"

    def get_context_data(self, **kwargs):
        context = super(FormDetail, self).get_context_data(**kwargs)
        published = Form.objects.published(for_user=self.request.user)
        try:
            context["form"] = published.get(slug=kwargs["slug"])
            return context
        except Form.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not context:
            return render(request, "forms/form_disabled.html", {})
        login_required = context["form"].login_required
        if login_required and not request.user.is_authenticated():
            path = urlquote(request.get_full_path())
            bits = (settings.LOGIN_URL, REDIRECT_FIELD_NAME, path)
            return redirect("%s?%s=%s" % bits)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        published = Form.objects.published(for_user=request.user)
        form = get_object_or_404(published, slug=kwargs["slug"])
        form_for_form = FormForForm(form, RequestContext(request),
                                    request.POST or None,
                                    request.FILES or None)
        if not form_for_form.is_valid():
            form_invalid.send(sender=request, form=form_for_form)
        else:
            # Attachments read must occur before model save,
            # or seek() will fail on large uploads.
            terms_update_user(request)
            attachments = []
            for f in form_for_form.files.values():
                f.seek(0)
                attachments.append((f.name, f.read()))
            entry = form_for_form.save()
            form_valid.send(sender=request, form=form_for_form, entry=entry)
            self.send_emails(request, form_for_form, form, entry, attachments)
            if not self.request.is_ajax():
                return redirect(form.redirect_url or
                    reverse("form_sent", kwargs={"slug": form.slug}))
        context = {"form": form, "form_for_form": form_for_form}
        return self.render_to_response(context)

    def render_to_response(self, context, **kwargs):
        if self.request.method == "POST" and self.request.is_ajax():
            json_context = json.dumps({
                "errors": context["form_for_form"].errors,
                "form": context["form_for_form"].as_p(),
                "message": context["form"].response,
            })
            if context["form_for_form"].errors:
                return HttpResponseBadRequest(json_context,
                    content_type="application/json")
            return HttpResponse(json_context, content_type="application/json")
        return super(FormDetail, self).render_to_response(context, **kwargs)

    def send_emails(self, request, form_for_form, form, entry, attachments):
        subject = form.email_subject
        if not subject:
            subject = "%s - %s" % (form.title, entry.entry_time)
        fields = []
        for (k, v) in form_for_form.fields.items():
            value = form_for_form.cleaned_data[k]
            if isinstance(value, list):
                value = ", ".join([i.strip() for i in value])
            fields.append((v.label, value))
        context = {
            "fields": fields,
            "message": form.email_message,
            "request": request,
        }
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = form_for_form.email_to()
        if email_to and form.send_email:
            send_mail_template(subject, "form_response", email_from,
                               email_to, context=context,
                               fail_silently=EMAIL_FAIL_SILENTLY)
        headers = None
        if email_to:
            headers = {"Reply-To": email_to}
        email_copies = split_choices(form.email_copies)
        if email_copies:
            send_mail_template(subject, "form_response_copies", email_from,
                               email_copies, context=context,
                               attachments=attachments,
                               fail_silently=EMAIL_FAIL_SILENTLY,
                               headers=headers)


form_detail = FormDetail.as_view()


def form_sent(request, slug, template="forms/form_sent.html"):
    """
    Show the response message.
    """
    published = Form.objects.published(for_user=request.user)
    context = {"form": get_object_or_404(published, slug=slug)}
    return render_to_response(template, context, RequestContext(request))


def forms_list(request, slug, template="forms/forms_list.html"):
    """
    Show forms list.
    """
    forms_list = FormsList.objects.get(slug=slug)
    forms = forms_list.forms.all().filter(
            Q(expiry_date__gte=datetime.datetime.now()) | Q(expiry_date__isnull=True), 
            Q(publish_date__lte=datetime.datetime.now()) | Q(publish_date__isnull=True), 
            status=2, 
    )
    external_forms = forms_list.external_forms.all().filter(
        Q(expiry_date__gte=datetime.datetime.now()) | Q(expiry_date__isnull=True), 
        Q(publish_date__lte=datetime.datetime.now()) | Q(publish_date__isnull=True), 
        status=2, 
    )
    context = {'forms_list': forms_list, 'forms': forms, 'external_forms': external_forms}
    return render(request, template, context)
