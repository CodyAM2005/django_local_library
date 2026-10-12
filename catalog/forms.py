import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class LibraryQuizForm(forms.Form):
    """Five-question quiz about the Local Library catalogue."""

    MODEL_CHOICES = [
        ('author', 'Author'),
        ('book', 'Book'),
        ('bookinstance', 'BookInstance'),
        ('genre', 'Genre'),
    ]

    q1 = forms.ChoiceField(
        label='Which model represents the person who writes a book?',
        choices=MODEL_CHOICES,
        widget=forms.RadioSelect,
    )
    q2 = forms.ChoiceField(
        label='Which model represents a specific copy of a book?',
        choices=MODEL_CHOICES,
        widget=forms.RadioSelect,
    )
    q3 = forms.ChoiceField(
        label='Which field uniquely identifies a book?',
        choices=[
            ('title', 'Title'),
            ('isbn', 'ISBN'),
            ('genre', 'Genre'),
        ],
        widget=forms.RadioSelect,
    )
    q4 = forms.ChoiceField(
        label='Which status means a copy can be borrowed?',
        choices=[
            ('available', 'Available'),
            ('on_loan', 'On loan'),
            ('maintenance', 'Maintenance'),
        ],
        widget=forms.RadioSelect,
    )
    q5 = forms.ChoiceField(
        label='Which relationship lets a book have multiple genres?',
        choices=[
            ('foreign_key', 'Foreign key'),
            ('many_to_many', 'Many-to-many'),
            ('one_to_one', 'One-to-one'),
        ],
        widget=forms.RadioSelect,
    )

    def score(self):
        answers = {
            'q1': 'author',
            'q2': 'bookinstance',
            'q3': 'isbn',
            'q4': 'available',
            'q5': 'many_to_many',
        }
        return sum(self.cleaned_data[question] == answer for question, answer in answers.items())


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data