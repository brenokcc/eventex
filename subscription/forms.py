#-*- coding: utf-8 -*-
from django import forms
from subscription.models import Subscription

from django.utils.translation import ugettext as _
from eventex.subscription import validators


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        exclude = ('created_at', 'paid', )
        
class MySubscriptionForm(forms.Form):
    name = forms.CharField(label=_('Nome'), max_length=100)
    cpf = forms.CharField(label=_('CPF'), max_length=11, min_length=11, validators=[validators.CpfValidator])
    email = forms.EmailField(label=_('E-mail'))
    phone = forms.CharField(label=_('Telefone'), required=False, max_length=20)
    
    def _unique_check(self, fieldname, error_message):
        param = { fieldname: self.cleaned_data[fieldname] }
        try: s = Subscription.objects.get(**param)
        except Subscription.DoesNotExist:
            return self.cleaned_data[fieldname]
        raise forms.ValidationError(error_message)
    def clean_cpf(self):
        return self._unique_check('cpf', _(u'CPF já inscrito.'))
    def clean_email(self):
        return self._unique_check('email', _(u'E-mail já inscrito.'))
    def clean(self):
        super(SubscriptionForm, self).clean()
        if not self.cleaned_data['email'] and not self.cleaned_data['phone']:
            raise forms.ValidationError(_(u'Você precisa informar seu e-mail ou seu telefone.'))
        return self.cleaned_data
