from django import forms
from .models import *


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nazwa księgi',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Opis (opcjonalnie)',
                'rows': 3,
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 63:
            raise forms.ValidationError("Nazwa księgi nie może przekraczać 63 znaków.")
        return name



class AccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pobierz użytkownika
        super().__init__(*args, **kwargs)

        # Filtrowanie ksiąg użytkownika
        if user and not user.is_superuser:
            self.fields['book'].queryset = Book.objects.filter(user=user)

        # Ustal typ konta (jeśli istnieje w danych)
        account_type = self.initial.get('account_type') or self.data.get('account_type') or getattr(self.instance, 'account_type', None)

        # Filtruj podtypy zgodnie z `account_type`
        valid_subtypes = Account.SUBTYPE_CATEGORIES.get(account_type, [])

        self.fields['account_subtype'].widget = forms.Select(
            choices=[(subtype, label) for subtype, label in Account.SUBTYPES if subtype in valid_subtypes],
            attrs={'class': 'form-control'}
        )

    class Meta:
        model = Account
        fields = ['name', 'description', 'account_type', 'account_subtype', 'initial_balance', 'book']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'account_type': forms.Select(attrs={'class': 'form-control'}),
            'initial_balance': forms.NumberInput(attrs={'class': 'form-control'}),
            'book': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nazwa konta',
            'description': 'Opis konta',
            'account_type': 'Typ konta',
            'account_subtype': 'Podtyp konta',
            'initial_balance': 'Saldo początkowe',
            'book': 'Księga',
        }
        help_texts = {
            'name': 'Podaj nazwę konta, np. "Konto bankowe" lub "Kasa".',
            'description': 'Krótki opis konta, np. "Konto do przechowywania gotówki".',
            'account_type': 'Wybierz typ konta, np. "Aktywa" lub "Pasywa".',
            'account_subtype': 'Wybierz podtyp konta, który pasuje do wybranego typu.',
            'initial_balance': 'Podaj początkowe saldo konta w PLN.',
            'book': 'Wybierz księgę, do której należy to konto.',
        }



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['name', 'description', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
        }
        labels = {
            'name': 'Nazwa kategorii',
            'description': 'Opis kategorii',
            'color': 'Kolor kategorii',
        }
        help_texts = {
            'name': 'Podaj nazwę kategorii, np. "Przychody" lub "Koszty".',
            'description': 'Krótki opis kategorii, np. "Koszty operacyjne".',
            'color': 'Wybierz kolor, który pomoże Ci wizualnie odróżnić tę kategorię.',
        }

class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pobierz użytkownika z argumentów
        super().__init__(*args, **kwargs)
        if user and not user.is_superuser:  # Filtrowanie kont i kategorii tylko dla zwykłych użytkowników
            self.fields['credit_account'].queryset = Account.objects.filter(user=user)
            self.fields['debit_account'].queryset = Account.objects.filter(user=user)
            self.fields['category'].queryset = Categories.objects.filter(user=user)

    class Meta:
        model = Transaction
        fields = ['description', 'amount', 'credit_account', 'debit_account', 'document', 'category', 'date']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'credit_account': forms.Select(attrs={'class': 'fordatem-control'}),
            'debit_account': forms.Select(attrs={'class': 'form-control'}),
            'document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'description': 'Opis transakcji',
            'amount': 'Kwota',
            'credit_account': 'Konto kredytowe',
            'debit_account': 'Konto debetowe',
            'document': 'Dokument',
            'category': 'Kategoria',
            'date': 'Data transakcji',
        }
        help_texts = {
            'description': 'Podaj szczegóły transakcji, np. "Zakup materiałów biurowych".',
            'amount': 'Podaj kwotę transakcji w PLN.',
            'credit_account': 'Wybierz konto, z którego środki zostały przelane (w przypadku kont aktywnych i kosztów), bądź na które zostały przelane (w przypadku kont pasywnych i przychodów).',
            'debit_account': 'Wybierz konto, na które środki zostały przelane (w przypadku kont aktywnych i kosztów), bądź z którego zostały przelane (w przypadku kont pasywnych i przychodów).',
            'document': 'Dodaj dokument potwierdzający transakcję, np. fakturę.',
            'category': 'Wybierz kategorię, do której należy ta transakcja.',
            'date': 'Wybierz datę, kiedy transakcja miała miejsce.',
        }

class BudgetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pobierz użytkownika z argumentów
        super().__init__(*args, **kwargs)
        if user and not user.is_superuser:  # Filtrowanie kategorii tylko dla zwykłych użytkowników
            self.fields['category'].queryset = Categories.objects.filter(user=user)

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
            'name': 'Nazwa budżetu',
            'description': 'Opis budżetu',
            'amount': 'Kwota budżetu',
            'start_date': 'Data rozpoczęcia',
            'end_date': 'Data zakończenia',
            'category': 'Kategoria',
        }
        help_texts = {
            'name': 'Podaj nazwę budżetu, np. "Budżet operacyjny".',
            'description': 'Krótki opis budżetu, np. "Budżet na wydatki biurowe".',
            'amount': 'Podaj całkowitą kwotę budżetu w PLN.',
            'start_date': 'Wybierz datę rozpoczęcia budżetu.',
            'end_date': 'Wybierz datę zakończenia budżetu.',
            'category': 'Wybierz kategorię, do której przypisany jest budżet.',
        }

class ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pobierz użytkownika
        super().__init__(*args, **kwargs)
        if user:
            # Filtrowanie ksiąg użytkownika
            self.fields['book'].queryset = Book.objects.filter(user=user)

    class Meta:
        model = Report
        fields = ['report_type', 'start_date', 'end_date', 'name', 'description', 'book']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'report_type': 'Typ raportu',
            'start_date': 'Data początkowa',
            'end_date': 'Data końcowa',
            'name': 'Nazwa raportu',
            'description': 'Opis raportu',
            'book': 'Księga',
        }
        help_texts = {
            'report_type': 'Wybierz typ raportu, np. "Bilans" lub "Rachunek zysków i strat".',
            'start_date': 'Wybierz datę początkową dla raportu.',
            'end_date': 'Wybierz datę końcową dla raportu.',
            'name': 'Podaj nazwę raportu, np. "Bilans za Q1 2025".',
            'description': 'Krótki opis raportu, np. "Bilans kwartalny".',
            'book': 'Wybierz księgę, z której dane mają być uwzględnione w raporcie.',
        }



class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['name', 'description', 'target_amount', 'deadline', 'deadline']
        widgets = {
            'name': forms.Textarea(attrs={'rows': 1, 'maxlength': 63}),
            'description': forms.TextInput(attrs={'maxlength': 255}),
            'target_amount': forms.NumberInput(attrs={'step': '0.01'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'name': 'Nazwa celu',
            'description': 'Opis celu',
            'target_amount': 'Docelowa kwota (PLN)',
            'account': 'Konto oszczędnościowe',
            'deadline': 'Termin realizacji',
            
        }
        help_texts = {
            'name': 'Podaj nazwę celu (maks. 63 znaki).',
            'description': 'Podaj krótki opis celu (maks. 255 znaków).',
            'target_amount': 'Podaj docelową kwotę oszczędności w PLN.',
            'account': 'Wybierz konto, na którym będą gromadzone oszczędności.',
            'deadline': 'Wybierz termin, do którego chcesz osiągnąć cel.',
        }