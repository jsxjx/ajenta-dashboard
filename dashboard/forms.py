from datetime import date, datetime
from django import forms
from datetimewidget.widgets import DateWidget


class UserForm(forms.Form):
    dateOptions = {
        'format': 'dd/mm/yyyy',
        'autoclose': True,
        'weekStart': 1,
        'startDate': '01/04/2013',
        'todayBtn': 'true',
    }

    start_date = forms.DateField(label='From', required=True, widget=DateWidget(options=dateOptions, bootstrap_version=3))
    end_date = forms.DateField(label='To', required=True, widget=DateWidget(options=dateOptions, bootstrap_version=3))

    def clean(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        if not all((start_date, end_date)):
            return self.cleaned_data

        if start_date > end_date:
            raise forms.ValidationError('End date must be after start date.')

        if start_date > date.today() or end_date > date.today():
            raise forms.ValidationError('You cannot select a future date.')

        return self.cleaned_data


class AdminForm(UserForm):
    tenant = forms.ChoiceField(label='Tenant')
    field_order = ['tenant', 'start_date', 'end_date']
