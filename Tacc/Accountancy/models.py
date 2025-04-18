from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


# Create your models here.
class Book(models.Model):
    name = models.TextField(max_length=63)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)  # lub inny odpowiedni mechanizm usuwania)
    def __str__(self):
        view = f"""
        <table>
            <tr>
                <td>{self.id}</td>
                <td>{self.name}</td>
                <td>{self.description}</td>
                <td>{self.created_at}</td>
                <td>{self.user}</td>
            </tr>
        </table>
        """
        return view




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
        view = f"""
        <table>
            <tr>
                <td>{self.id}</td>
                <td>{self.name}</td>
                <td>{self.description}</td>
                <td>{self.account_type}</td>
                <td>{self.account_subtype}</td>
                <td>{self.initial_balance}</td>
                <td>{self.created_at}</td>
                <td>{self.book}</td>
                <td>{self.user}</td>
            </tr>
        </table>
        """
        return view


class Transaction(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    credit_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    debit_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='debit_account')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/', blank=True, null=True)
    category = models.ForeignKey('Categories', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        view = f"""
        <table>
            <tr>
                <td>{self.id}</td>
                <td>{self.date}</td>
                <td>{self.description}</td>
                <td>{self.amount}</td>
                <td>{self.account}</td>
                <td>{self.category}</td>
                <td>{self.created_at}</td>
            </tr>
        </table>
        """
        return view



class Categories(models.Model):
    name = models.TextField(max_length=63)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=7, default="#000000")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        view = f"""
        <table>
            <tr>
                <td>{self.id}</td>
                <td>{self.name}</td>
                <td>{self.description}</td>
                <td>{self.created_at}</td>
                <td>{self.user}</td>
            </tr>
        </table>
        """
        return view