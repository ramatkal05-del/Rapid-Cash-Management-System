from django import forms
from .models import Expense
from core.models import Currency

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'currency', 'reason', 'category', 'destination', 'comment']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'block w-full rounded-lg border-slate-200 text-sm focus:ring-brand-500 focus:border-brand-500'}),
            'currency': forms.Select(attrs={'class': 'block w-full rounded-lg border-slate-200 text-sm focus:ring-brand-500 focus:border-brand-500'}),
            'reason': forms.TextInput(attrs={'class': 'block w-full rounded-lg border-slate-200 text-sm focus:ring-brand-500 focus:border-brand-500', 'placeholder': 'e.g. Loyer, Internet, Transport...'}),
            'category': forms.TextInput(attrs={'class': 'block w-full rounded-lg border-slate-200 text-sm focus:ring-brand-500 focus:border-brand-500', 'placeholder': 'e.g. Logistique, RH, IT...'}),
            'destination': forms.TextInput(attrs={'class': 'block w-full rounded-lg border-slate-200 text-sm focus:ring-brand-500 focus:border-brand-500'}),
            'comment': forms.Textarea(attrs={'class': 'block w-full rounded-lg border-slate-200 text-sm focus:ring-brand-500 focus:border-brand-500', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure currencies are loaded
        self.fields['currency'].queryset = Currency.objects.all()
