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

    SUBTYPES = [
        ('fixed', 'Trwałe'),
        ('current', 'Obrotowe'),
        ('financial', 'Środki pieniężne'),
        ('inventories', 'Zapasy'),
        ('receivables', 'Należności'),
        ('long_term', 'Długoterminowe'),
        ('short_term', 'Krótkoterminowe'),
        ('equity', 'Kapitał własny'),
        ('fixed_incomes', 'Stałe'),
        ('variable_incomes', 'Zmienne'),
        ('passive', 'Pasywne'),
        ('fixed_expenses', 'Stałe'),
        ('variable_expenses', 'Zmienne'),
        ('unpredicted', 'Nieprzewidywalne'),
    ]

    SUBTYPE_CATEGORIES = {
        'assets': ['fixed', 'current', 'financial', 'inventories', 'receivables'],
        'liabilities': ['long_term', 'short_term', 'equity'],
        'revenue': ['fixed_incomes', 'variable_incomes', 'passive'],
        'expenses': ['fixed_expenses', 'variable_expenses', 'unpredicted'],
 }

    name = models.TextField(max_length=63)
    description = models.CharField(max_length=255, blank=True, null=True)
    account_type = models.CharField(max_length=63, choices=TYPES)
    account_subtype = models.CharField(max_length=63, choices=SUBTYPES, blank=True, null=True)
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def clean(self):
        if self.account_type and self.account_subtype:
            valid_subtype_keys = self.SUBTYPE_CATEGORIES.get(self.account_type, [])
            if self.account_subtype not in valid_subtype_keys:
                raise ValidationError(f"Nieprawidłowy podtyp '{self.account_subtype}' dla typu konta '{self.account_type}'.")

    def __str__(self):
        return f'{self.account_type} {self.account_subtype}\t{self.name}'

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
        """
        Oblicza saldo konta zgodnie z zasadami księgowania na kontach T,
        uwzględniając initial_balance także dla przychodów i wydatków.
        """
        try:
            debit_sum = self.debit_transactions.aggregate(models.Sum('amount'))['amount__sum'] or 0
            credit_sum = self.credit_transactions.aggregate(models.Sum('amount'))['amount__sum'] or 0

            if self.account_type == 'assets':  # Aktywa
                return self.initial_balance + debit_sum - credit_sum
            elif self.account_type == 'liabilities':  # Pasywa
                return self.initial_balance - debit_sum + credit_sum
            elif self.account_type == 'revenue':  # Przychody
                return self.initial_balance + credit_sum - debit_sum
            elif self.account_type == 'expenses':  # Wydatki
                return self.initial_balance + debit_sum - credit_sum
            elif self.account_type == 'equity':  # Kapitał własny
                return self.initial_balance + credit_sum - debit_sum
            else:
                return self.initial_balance + debit_sum - credit_sum
        except DatabaseError as e:
            return self.initial_balance
    def calculate_balance_in_date_range(self, start_date, end_date):
        """
        Oblicza saldo konta w zadanym przedziale czasowym.
        Uwzględnia tylko transakcje w zadanym zakresie dat.
        """
        try:
            # Filtruj transakcje według zakresu dat
            debit_sum = self.debit_transactions.filter(
                date__gte=start_date,
                date__lte=end_date
            ).aggregate(models.Sum('amount'))['amount__sum'] or 0

            credit_sum = self.credit_transactions.filter(
                date__gte=start_date,
                date__lte=end_date
            ).aggregate(models.Sum('amount'))['amount__sum'] or 0

            if self.account_type == 'assets':  # Aktywa
                return debit_sum - credit_sum  # Tylko transakcje z okresu, bez stanu początkowego
            elif self.account_type == 'liabilities':  # Pasywa
                return credit_sum - debit_sum  # Tylko transakcje z okresu, bez stanu początkowego
            elif self.account_type == 'revenue':  # Przychody
                return credit_sum - debit_sum  # Tylko transakcje z okresu, bez stanu początkowego
            elif self.account_type == 'expenses':  # Wydatki
                return debit_sum - credit_sum  # Tylko transakcje z okresu, bez stanu początkowego
            else:
                return debit_sum - credit_sum  # Tylko transakcje z okresu, bez stanu początkowego
        except DatabaseError as e:
            return 0

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
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Dodanie pola book

    def __str__(self):
        return self.name

    def generate_report(self):
        """
        Generuje raport w zależności od typu raportu (report_type) z uwzględnieniem zakresu dat.
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
        Uwzględnia tylko konta z wybranej księgi i transakcje w zakresie dat raportu.
        """
        assets = Account.objects.filter(account_type='assets', user=self.user, book=self.book)
        liabilities = Account.objects.filter(account_type='liabilities', user=self.user, book=self.book)

        assets_balances = {}
        for account in assets:
            # Oblicz saldo uwzględniając tylko transakcje w zakresie dat raportu
            balance = account.calculate_balance_in_date_range(self.start_date, self.end_date)
            assets_balances[account.name] = balance

        liabilities_balances = {}
        for account in liabilities:
            # Oblicz saldo uwzględniając tylko transakcje w zakresie dat raportu
            balance = account.calculate_balance_in_date_range(self.start_date, self.end_date)
            liabilities_balances[account.name] = balance

        assets_total = sum(assets_balances.values())
        liabilities_total = sum(liabilities_balances.values())

        return {
            'type': 'Bilans',
            'assets': assets_balances,
            'liabilities': liabilities_balances,
            'total_assets': assets_total,
            'total_liabilities': liabilities_total,
            'equity': assets_total - liabilities_total,
        }

    def _generate_income_statement(self):
        """
        Generuje rachunek zysków i strat jako słownik.
        Uwzględnia tylko konta z wybranej księgi i transakcje w zakresie dat raportu.
        """
        revenues = Account.objects.filter(account_type='revenue', user=self.user, book=self.book)
        expenses = Account.objects.filter(account_type='expenses', user=self.user, book=self.book)

        revenues_balances = {}
        for account in revenues:
            # Oblicz saldo uwzględniając tylko transakcje w zakresie dat raportu
            balance = account.calculate_balance_in_date_range(self.start_date, self.end_date)
            revenues_balances[account.name] = balance

        expenses_balances = {}
        for account in expenses:
            # Oblicz saldo uwzględniając tylko transakcje w zakresie dat raportu
            balance = account.calculate_balance_in_date_range(self.start_date, self.end_date)
            expenses_balances[account.name] = balance

        total_revenues = sum(revenues_balances.values())
        total_expenses = sum(expenses_balances.values())

        return {
            'type': 'Rachunek zysków i strat',
            'revenues': revenues_balances,
            'expenses': expenses_balances,
            'net_income': total_revenues - total_expenses,
        }

    def _generate_cash_flow_statement(self):
        """
        Generuje rachunek przepływów pieniężnych jako słownik.
        Uwzględnia tylko konta z wybranej księgi i transakcje w zakresie dat raportu.
        """
        accounts = Account.objects.filter(account_type='assets', account_subtype='financial', user=self.user, book=self.book)

        cash_flows = {}
        for account in accounts:
            # Oblicz saldo uwzględniając tylko transakcje w zakresie dat raportu
            balance = account.calculate_balance_in_date_range(self.start_date, self.end_date)
            cash_flows[account.name] = balance

        total_cash_flow = sum(cash_flows.values())

        return {
            'type': 'Rachunek przepływów pieniężnych',
            'cash_flows': cash_flows,
            'total_cash_flow': total_cash_flow,
        }