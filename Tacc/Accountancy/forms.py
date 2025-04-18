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

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction  # Zmień na odpowiedni model transakcji
        fields = ['description', 'amount', 'credit_account', 'debit_account', 'document', 'category']  # Zmień na odpowiednie pola modelu transakcji
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'credit_account': forms.Select(attrs={'class': 'form-control'}),
            'debit_account': forms.Select(attrs={'class': 'form-control'}),
            'document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'description': 'Opis',
            'amount': 'Kwota',
            'credit_account': 'Konto kredytowe',
            'debit_account': 'Konto debetowe',
            'document': 'Dokument',
            'category': 'Kategoria',
        }



class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budgets
        fields = ['name', 'description', 'amount', 'start_date', 'end_date', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nazwa',
            'description': 'Opis',
            'amount': 'Kwota',
            'start_date': 'Data rozpoczęcia',
            'end_date': 'Data zakończenia',
            'category': 'Kategoria',
        }

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_type', 'start_date', 'end_date', 'name', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'report_type': 'Typ raportu',
            'start_date': 'Data początkowa',
            'end_date': 'Data końcowa',
            'name': 'Nazwa',
            'description': 'Opis',
        }
