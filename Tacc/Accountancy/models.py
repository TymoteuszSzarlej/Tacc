from django.db import models, DatabaseError
from django.conf import settings
from django.core.exceptions import ValidationError



# Create your models here.
class Book(models.Model):
    name = models.TextField(max_length=63)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)  # lub inny odpowiedni mechanizm usuwania)
    def __str__(self):
        return self.name




class Account(models.Model):
    TYPES = [
        ('assets', 'Aktywa'),
        ('liabilities', 'Pasywa'),
        ('revenue', 'Przychody'),
        ('expenses', 'Koszty'),
    ]

    SUBTYPES = {
        'assets': [
            ('fixed', 'Trwałe'),
            ('current', 'Obrotowe'),
            ('financial', 'Środki pieniężne'),
            ('inventories', 'Zapasy'),
            ('receivables', 'Należności'),
        ],
        'liabilities': [
            ('long_term', 'Długoterminowe'),
            ('short_term', 'Krótkoterminowe'),
            ('equity', 'Kapitał własny'),
        ],
        'revenue': [],
        'expenses': [],

    }

    name = models.TextField(max_length=63)
    description = models.CharField(max_length=255, blank=True, null=True)
    account_type = models.CharField(max_length=63, choices=TYPES)
    account_subtype = models.CharField(max_length=63, choices=SUBTYPES)
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def clean(self):
        if self.account_type and self.account_subtype:
            valid_subtypes = dict(self.SUBTYPES).get(self.account_type, [])
            valid_subtype_keys = [s[0] for s in valid_subtypes]
            if self.account_subtype not in valid_subtype_keys:
                raise ValidationError(f"Nieprawidłowy podtyp '{self.account_subtype}' dla typu konta '{self.account_type}'.")


    def __str__(self):
        return self.name

    def get_debit_transactions(self):
        """
        Zwraca listę transakcji, w których to konto jest kontem debetowym.
        """
        return self.debit_transactions.all()  # Użyj related_name 'debit_transactions'

    def get_credit_transactions(self):
        """
        Zwraca listę transakcji, w których to konto jest kontem kredytowym.
        """
        return self.credit_transactions.all()  # Użyj related_name 'credit_transactions'

    def calculate_balance(self):
        try:
            debit_sum = self.debit_transactions.aggregate(models.Sum('amount'))['amount__sum'] or 0
            credit_sum = self.credit_transactions.aggregate(models.Sum('amount'))['amount__sum'] or 0
            return self.initial_balance + debit_sum - credit_sum
        except DatabaseError as e:
            # Możesz zalogować błąd lub zwrócić domyślną wartość
            return self.initial_balance

class Transaction(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    credit_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='credit_transactions'  # Dodaj related_name
    )
    debit_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='debit_transactions'
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/', blank=True, null=True)
    category = models.ForeignKey('Categories', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description or f"Transaction {self.id}"



class Categories(models.Model):
    name = models.TextField(max_length=63)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=7, default="#000000")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Budgets(models.Model):
    name = models.TextField(max_length=63)
    description = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Report(models.Model):
    REPORT_TYPES = [
        ('balance_sheet', 'Bilans'),
        ('income_statement', 'Rachunek zysków i strat'),
        ('cash_flow_statement', 'Rachunek przepływów pieniężnych'),
    ]

    report_type = models.CharField(max_length=63, choices=REPORT_TYPES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    name = models.TextField(max_length=63)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def generate_report(self):
        """
        Generuje raport w zależności od typu raportu (report_type).
        """
        if self.report_type == 'balance_sheet':
            return self._generate_balance_sheet()
        elif self.report_type == 'income_statement':
            return self._generate_income_statement()
        elif self.report_type == 'cash_flow_statement':
            return self._generate_cash_flow_statement()
        else:
            return {'error': 'Nieznany typ raportu'}

    def _generate_balance_sheet(self):
        """
        Generuje bilans jako słownik.
        """
        assets = Account.objects.filter(account_type='assets')
        liabilities = Account.objects.filter(account_type='liabilities')

        assets_total = sum([account.calculate_balance() for account in assets])
        liabilities_total = sum([account.calculate_balance() for account in liabilities])

        return {
            'type': 'Bilans',
            'assets': {account.name: account.calculate_balance() for account in assets},
            'liabilities': {account.name: account.calculate_balance() for account in liabilities},
            'total_assets': assets_total,
            'total_liabilities': liabilities_total,
            'equity': assets_total - liabilities_total,
        }

    def _generate_income_statement(self):
        """
        Generuje rachunek zysków i strat jako słownik.
        """
        revenues = Account.objects.filter(account_type='revenue')
        expenses = Account.objects.filter(account_type='expenses')

        total_revenues = sum([account.calculate_balance() for account in revenues])
        total_expenses = sum([account.calculate_balance() for account in expenses])

        return {
            'type': 'Rachunek zysków i strat',
            'revenues': {account.name: account.calculate_balance() for account in revenues},
            'expenses': {account.name: account.calculate_balance() for account in expenses},
            'net_income': total_revenues - total_expenses,
        }

    def _generate_cash_flow_statement(self):
        """
        Generuje rachunek przepływów pieniężnych jako słownik.
        """
        accounts = Account.objects.filter(account_type='assets', account_subtype='financial')

        cash_flows = {account.name: account.calculate_balance() for account in accounts}
        total_cash_flow = sum(cash_flows.values())

        return {
            'type': 'Rachunek przepływów pieniężnych',
            'cash_flows': cash_flows,
            'total_cash_flow': total_cash_flow,
        }