from django import forms

class SignUpForm(forms.Form):
	username = forms.CharField(label='Username', max_length=100)
	fname = forms.CharField(label='First name', max_length=100)
	lname = forms.CharField(label='Last name', max_length=100)
	location = forms.CharField(label='Location', max_length=100)
	email = forms.CharField(label='Email', max_length=100)
	bio = forms.CharField(label='Bio', max_length=100)
	pw = forms.CharField(label='Password', max_length=100)

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=100)
	pw = forms.CharField(label='Password', max_length=100)
