from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from .forms import *

# Create your views here.
def books(request):
    user = User.objects.get(username=request.user)
    books = Book.objects.all().filter(user=user)
    
    return render(request, 'Accountancy/books/main.html.jinja', {'books': books})



def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)  # Nie zapisuj automatycznie w bazie danych
            book.user = request.user       # Ustaw użytkownika na zalogowanego użytkownika
            book.save()                    # Zapisz obiekt w bazie danych
            return redirect('books')   # Przekieruj użytkownika po zapisaniu
    else:
        form = BookForm()
    return render(request, 'Accountancy/books/create.html.jinja', {'form': form})

def book_details(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'Accountancy/books/details.html.jinja', {'book': book})

def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books')
    else:
        form = BookForm(instance=book)
    return render(request, 'Accountancy/books/edit.html.jinja', {'form': form, 'book': book})

def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('books')
    return render(request, 'Accountancy/books/delete.html.jinja', {'book': book})

def accounts(request):
    user = User.objects.get(username=request.user)
    accounts = Account.objects.all().filter(user=user)
    
    return render(request, 'Accountancy/accounts/main.html.jinja', {'accounts': accounts})

def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)  # Nie zapisuj automatycznie w bazie danych
            account.user = request.user       # Ustaw użytkownika na zalogowanego użytkownika
            account.save()                    # Zapisz obiekt w bazie danych
            return redirect('accounts')   # Przekieruj użytkownika po zapisaniu
    else:
        form = AccountForm()
    return render(request, 'Accountancy/accounts/create.html.jinja', {'form': form})

def account_details(request, account_id):
    account = Account.objects.get(id=account_id)
    return render(request, 'Accountancy/accounts/details.html.jinja', {'account': account})
def edit_account(request, account_id):
    account = Account.objects.get(id=account_id)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('accounts')
    else:
        form = AccountForm(instance=account)
    return render(request, 'Accountancy/accounts/edit.html.jinja', {'form': form, 'account': account})
def delete_account(request, account_id):
    account = Account.objects.get(id=account_id)
    if request.method == 'POST':
        account.delete()
        return redirect('accounts')
    return render(request, 'Accountancy/accounts/delete.html.jinja', {'account': account})

def categories(request):
    user = User.objects.get(username=request.user)
    categories = Categories.objects.all().filter(user=user)
    
    return render(request, 'Accountancy/categories/main.html.jinja', {'categories': categories})
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)  # Nie zapisuj automatycznie w bazie danych
            category.user = request.user       # Ustaw użytkownika na zalogowanego użytkownika
            category.save()                    # Zapisz obiekt w bazie danych
            return redirect('categories')   # Przekieruj użytkownika po zapisaniu
    else:
        form = CategoryForm()
    return render(request, 'Accountancy/categories/create.html.jinja', {'form': form})
def category_details(request, category_id):
    category = Categories.objects.get(id=category_id)
    return render(request, 'Accountancy/categories/details.html.jinja', {'category': category})
def edit_category(request, category_id):
    category = Categories.objects.get(id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'Accountancy/categories/edit.html.jinja', {'form': form, 'category': category})
def delete_category(request, category_id):
    category = Categories.objects.get(id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('categories')
    return render(request, 'Accountancy/categories/delete.html.jinja', {'category': category})

def transactions(request):
    user = User.objects.get(username=request.user)
    transactions = Transaction.objects.all().filter(user=user)
    
    return render(request, 'Accountancy/transactions/main.html.jinja', {'transactions': transactions})
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)  # Nie zapisuj automatycznie w bazie danych
            transaction.user = request.user       # Ustaw użytkownika na zalogowanego użytkownika
            transaction.save()                    # Zapisz obiekt w bazie danych
            return redirect('transactions')   # Przekieruj użytkownika po zapisaniu
    else:
        form = TransactionForm()
    return render(request, 'Accountancy/transactions/create.html.jinja', {'form': form})
def transaction_details(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    return render(request, 'Accountancy/transactions/details.html.jinja', {'transaction': transaction})
def edit_transaction(request, transaction_id):  
    transaction = Transaction.objects.get(id=transaction_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transactions')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'Accountancy/transactions/edit.html.jinja', {'form': form, 'transaction': transaction})
def delete_transaction(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transactions')
    return render(request, 'Accountancy/transactions/delete.html.jinja', {'transaction': transaction})