from datetime import date
from django import forms
from datetimewidget.widgets import DateWidget


class UserForm(forms.Form):
    start_date = forms.DateField(label='From', required=True, widget=DateWidget(bootstrap_version=3))
    end_date = forms.DateField(label='To', required=True, widget=DateWidget(bootstrap_version=3))

    def clean(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        if not all((start_date, end_date)):
            return self.cleaned_data

        if start_date < date(2013, 04, 01) or end_date < date(2013, 04, 01):
            raise forms.ValidationError(message='There is no data before 01/04/2013.')

        if start_date > date.today() or end_date > date.today():
            raise forms.ValidationError('You cannot select a future date.')

        if start_date > end_date:
            raise forms.ValidationError('End date must be after start date.')

        return self.cleaned_data


class AdminForm(UserForm):
    tenant = forms.ChoiceField(label='Tenant')
    field_order = ['tenant', 'start_date', 'end_date']
