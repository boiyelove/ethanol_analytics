from django import forms
from django.core.mail import send_mail
from django.conf import settings


class FormLink:
	def __init__(self, text, url):
		self.name = text
		self.url = url

	def __str__(self):
		return self.name


class BugReportForm(forms.Form):
	title = forms.CharField(max_length=100)
	detail = forms.CharField(widget=forms.Textarea)

	def clean_detail(self):
		detail = self.cleaned_data.get('detail')
		detail_list = detail.split(' ')
		if len(detail_list) <= 5:
			raise forms.ValidationError('Please provide more detail about the bug')
		return detail

	def send_bug_report(self):
		return send_mail(subject=self.cleaned_data.get('title'),
		message = self.cleaned_data.get('detail'),
		recipient_list = [settings.DEFAULT_TO_EMAIL],
		from_email = settings.DEFAULT_FROM_EMAIL)


