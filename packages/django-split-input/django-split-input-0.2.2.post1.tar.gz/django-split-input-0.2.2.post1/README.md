# django_split_input

## About

This is a django widget for multiple fixed size inputs for one form field. These could be used for those super fancy
verification code forms. The cursor is moved to the next input field using JS/jQuery.

![django_split_input Showcase](django_split_input_showcase.png)

## Usage

1. Install `django_split_input` and add it to your `INSTALLED_APPS`.
   ```shell
   pip install django-split-input
   ```
   In your settings.py:
   ```python
   "django_split_input",
   ```
2. Install `jQuery` using your preferred method (e.g.
   [django-yarnpkg](https://pypi.org/project/django-yarnpkg/))
   
3. Create a form with a `CharField`.
4. Use `SplitInput` as a widget and supply the sizes of all input fields.

```python
from django import forms
from django_split_input import SplitInput


class VerificationForm(forms.Form):
   auth_code = forms.CharField(label='Code', widget=SplitInput(sizes=(3, 3, 3)))
```

