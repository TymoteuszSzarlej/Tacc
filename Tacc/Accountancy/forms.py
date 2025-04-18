from django import forms
from .models import *

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account  # Zmień na odpowiedni model konta
        fields = ['name', 'description', 'account_type', 'account_subtype', 'initial_balance', 'book']  # Zmień na odpowiednie pola modelu konta
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'account_type': forms.Select(attrs={'class': 'form-control'}),
            'account_subtype': forms.Select(attrs={'class': 'form-control'}),
            'initial_balance': forms.NumberInput(attrs={'class': 'form-control'}),
            'book': forms.Select(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories  # Zmień na odpowiedni model kategorii
        fields = ['name', 'description', 'color']  # Zmień na odpowiednie pola modelu kategorii
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
        }