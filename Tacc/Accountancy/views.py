from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from datetime import datetime, timedelta
from django.db.models import Sum


# Create your views here.
@login_required
def books(request):
    books = Book.objects.filter(user=request.user)  # Filtrowanie książek użytkownika
    return render(request, 'Accountancy/books/main.html.jinja', {'books': books})

@login_required
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user  # Przypisanie książki do użytkownika
            book.save()
            return redirect('books')
    else:
        form = BookForm()
    return render(request, 'Accountancy/books/create.html.jinja', {'form': form})

@login_required
def book_details(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)  # Sprawdzenie właściciela książki
    return render(request, 'Accountancy/books/details.html.jinja', {'book': book})

@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)  # Sprawdzenie właściciela książki
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books')
    else:
        form = BookForm(instance=book)
    return render(request, 'Accountancy/books/edit.html.jinja', {'form': form, 'book': book})

@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)  # Sprawdzenie właściciela książki
    if request.method == 'POST':
        book.delete()
        return redirect('books')
    return render(request, 'Accountancy/books/delete.html.jinja', {'book': book})

@login_required
def accounts(request):
    accounts = Account.objects.filter(user=request.user)  # Filtrowanie kont użytkownika
    return render(request, 'Accountancy/accounts/main.html.jinja', {'accounts': accounts})

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, user=request.user)  # Przekazanie użytkownika do formularza
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user  # Przypisanie konta do użytkownika
            account.save()
            return redirect('accounts')
    else:
        form = AccountForm(user=request.user)  # Przekazanie użytkownika do formularza
    return render(request, 'Accountancy/accounts/create.html.jinja', {'form': form})

@login_required
def account_details(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)  # Sprawdzenie właściciela konta
    return render(request, 'Accountancy/accounts/details.html.jinja', {
        'account': account,
        'credits': account.get_credit_transactions(),
        'debits': account.get_debit_transactions()
    })

@login_required
def edit_account(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)  # Sprawdzenie właściciela konta
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account, user=request.user)  # Przekazanie użytkownika do formularza
        if form.is_valid():
            form.save()
            return redirect('accounts')
    else:
        form = AccountForm(instance=account, user=request.user)  # Przekazanie użytkownika do formularza
    return render(request, 'Accountancy/accounts/edit.html.jinja', {'form': form, 'account': account})

@login_required
def delete_account(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)  # Sprawdzenie właściciela konta
    if request.method == 'POST':
        account.delete()
        return redirect('accounts')
    return render(request, 'Accountancy/accounts/delete.html.jinja', {'account': account})

@login_required
def categories(request):
    user = User.objects.get(username=request.user)
    categories = Categories.objects.all().filter(user=user)
    return render(request, 'Accountancy/categories/main.html.jinja', {'categories': categories})

@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('categories')
    else:
        form = CategoryForm()
    return render(request, 'Accountancy/categories/create.html.jinja', {'form': form})

@login_required
def category_details(request, category_id):
    category = Categories.objects.get(id=category_id)
    return render(request, 'Accountancy/categories/details.html.jinja', {'category': category})

@login_required
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

@login_required
def delete_category(request, category_id):
    category = Categories.objects.get(id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('categories')
    return render(request, 'Accountancy/categories/delete.html.jinja', {'category': category})

@login_required
def transactions(request):
    transactions = Transaction.objects.filter(user=request.user)  # Filtrowanie transakcji użytkownika
    return render(request, 'Accountancy/transactions/main.html.jinja', {'transactions': transactions})

@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)  # Przekazanie użytkownika do formularza
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user  # Przypisanie transakcji do użytkownika
            transaction.save()
            return redirect('transactions')
    else:
        form = TransactionForm(user=request.user)  # Przekazanie użytkownika do formularza
    return render(request, 'Accountancy/transactions/create.html.jinja', {'form': form})

@login_required
def transaction_details(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    return render(request, 'Accountancy/transactions/details.html.jinja', {'transaction': transaction})

@login_required
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)  # Sprawdzenie właściciela transakcji
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, user=request.user)  # Przekazanie użytkownika do formularza
        if form.is_valid():
            form.save()
            return redirect('transactions')
    else:
        form = TransactionForm(instance=transaction, user=request.user)  # Przekazanie użytkownika do formularza
    return render(request, 'Accountancy/transactions/edit.html.jinja', {'form': form, 'transaction': transaction})

@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)  # Sprawdzenie właściciela transakcji
    if request.method == 'POST':
        transaction.delete()
        return redirect('transactions')
    return render(request, 'Accountancy/transactions/delete.html.jinja', {'transaction': transaction})

@login_required
def budgets(request):
    user = User.objects.get(username=request.user)
    budgets = Budgets.objects.all().filter(user=user)
    return render(request, 'Accountancy/budgets/main.html.jinja', {'budgets': budgets})

@login_required
def create_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('budgets')
    else:
        form = BudgetForm()
    return render(request, 'Accountancy/budgets/create.html.jinja', {'form': form})

@login_required
def budget_details(request, budget_id):
    budget = Budgets.objects.get(id=budget_id)
    return render(request, 'Accountancy/budgets/details.html.jinja', {'budget': budget})

@login_required
def edit_budget(request, budget_id):
    budget = Budgets.objects.get(id=budget_id)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('budgets')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'Accountancy/budgets/edit.html.jinja', {'form': form, 'budget': budget})

@login_required
def delete_budget(request, budget_id):
    budget = Budgets.objects.get(id=budget_id)
    if request.method == 'POST':
        budget.delete()
        return redirect('budgets')
    return render(request, 'Accountancy/budgets/delete.html.jinja', {'budget': budget})

@login_required
def reports(request):
    user = User.objects.get(username=request.user)
    reports = Report.objects.all().filter(user=user)
    return render(request, 'Accountancy/reports/main.html.jinja', {'reports': reports})

@login_required
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, user=request.user)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user  # Przypisz użytkownika!
            report.save()
            return redirect('reports')
    else:
        form = ReportForm(user=request.user)
    return render(request, 'Accountancy/reports/create.html.jinja', {'form': form})

@login_required
def report_details(request, report_id):
    # Pobranie raportu przypisanego do zalogowanego użytkownika
    report = get_object_or_404(Report, id=report_id, user=request.user)

    # Pobranie wybranej księgi
    book = report.book

    # Generowanie danych raportu na podstawie wybranej księgi
    accounts = Account.objects.filter(user=request.user, book=book)
    transactions = Transaction.objects.filter(user=request.user, credit_account__book=book, debit_account__book=book)

    # Przykład dodatkowego przetwarzania danych raportu
    total_assets = accounts.filter(account_type='assets').aggregate(Sum('initial_balance'))['initial_balance__sum'] or 0
    total_liabilities = accounts.filter(account_type='liabilities').aggregate(Sum('initial_balance'))['initial_balance__sum'] or 0
    total_revenues = transactions.filter(credit_account__account_type='revenue').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = transactions.filter(debit_account__account_type='expenses').aggregate(Sum('amount'))['amount__sum'] or 0

    report_data = report.generate_report()

    context = {
        'report': report,
        'report_data': report_data,
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'total_revenues': total_revenues,
        'total_expenses': total_expenses,
    }

    return render(request, 'Accountancy/reports/details.html.jinja', context)

@login_required
def edit_report(request, report_id):
    report = get_object_or_404(Report, id=report_id, user=request.user)
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report, user=request.user)
        if form.is_valid():
            edited_report = form.save(commit=False)
            edited_report.user = request.user  # Przypisz użytkownika!
            edited_report.save()
            return redirect('reports')
    else:
        form = ReportForm(instance=report, user=request.user)
    return render(request, 'Accountancy/reports/edit.html.jinja', {'form': form, 'report': report})

@login_required
def delete_report(request, report_id):
    report = Report.objects.get(id=report_id)
    if request.method == 'POST':
        report.delete()
        return redirect('reports')
    return render(request, 'Accountancy/reports/delete.html.jinja', {'report': report})

@login_required
def report_pdf(request, report_id):
    report = Report.objects.get(id=report_id)
    return render(request, 'Accountancy/reports/pdf.html.jinja', {'report': report})

@login_required
def financial_analysis(request):
    assets = Account.objects.filter(account_type='assets')
    liabilities = Account.objects.filter(account_type='liabilities')
    revenues = Account.objects.filter(account_type='revenue')
    expenses = Account.objects.filter(account_type='expenses')
    equity = Account.objects.filter(account_type='equity')

    total_assets = sum([account.calculate_balance() for account in assets])
    total_liabilities = sum([account.calculate_balance() for account in liabilities])
    total_revenues = sum([account.calculate_balance() for account in revenues])
    total_expenses = sum([account.calculate_balance() for account in expenses])
    total_equity = sum([account.calculate_balance() for account in equity])

    ros = (total_revenues - total_expenses) / total_revenues * 100 if total_revenues else 0
    roa = (total_revenues - total_expenses) / total_assets * 100 if total_assets else 0
    roe = (total_revenues - total_expenses) / total_equity * 100 if total_equity else 0

    current_assets = sum([account.calculate_balance() for account in assets if account.account_subtype == 'current'])
    current_liabilities = sum([account.calculate_balance() for account in liabilities if account.account_subtype == 'current'])
    current_ratio = current_assets / current_liabilities if current_liabilities else 0
    quick_ratio = (current_assets - sum([account.calculate_balance() for account in assets if account.account_subtype == 'inventory'])) / current_liabilities if current_liabilities else 0

    debt_ratio = total_liabilities / total_assets * 100 if total_assets else 0

    context = {
        'ros': ros,
        'roa': roa,
        'roe': roe,
        'current_ratio': current_ratio,
        'quick_ratio': quick_ratio,
        'debt_ratio': debt_ratio,
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'total_revenues': total_revenues,
        'total_expenses': total_expenses,
        'total_equity': total_equity,
    }

    return render(request, 'Accountancy/analysis/financial_analysis.html.jinja', context)

@login_required
def financial_forecast(request):
    user = request.user

    total_revenues = Transaction.objects.filter(
        credit_account__account_type='revenue',
        user=user
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    total_expenses = Transaction.objects.filter(
        debit_account__account_type='expenses',
        user=user
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    total_assets = Account.objects.filter(
        account_type='assets',
        user=user
    ).aggregate(Sum('initial_balance'))['initial_balance__sum'] or 0

    total_liabilities = Account.objects.filter(
        account_type='liabilities',
        user=user
    ).aggregate(Sum('initial_balance'))['initial_balance__sum'] or 0

    today = datetime.today()
    forecast_data = {
        'dates': [(today + timedelta(days=i * 30)).strftime('%Y-%m') for i in range(12)],
        'revenues': [],
        'expenses': [],
        'profits': [],
    }

    for i in range(12):
        forecast_revenue = float(total_revenues) * (1 + 0.02 * i)
        forecast_expense = float(total_expenses) * (1 + 0.015 * i)
        forecast_profit = forecast_revenue - forecast_expense

        forecast_data['revenues'].append(round(forecast_revenue, 2))
        forecast_data['expenses'].append(round(forecast_expense, 2))
        forecast_data['profits'].append(round(forecast_profit, 2))

    return render(request, 'Accountancy/forecast/financial_forecast.html.jinja', {
        'forecast_data': forecast_data,
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
    })

@login_required
def dashboard(request):
    # Sprawdzenie, czy użytkownik ma jakiekolwiek księgi
    if not Book.objects.filter(user=request.user).exists():
        # Tworzenie "KSIĘGI GŁÓWNEJ"
        main_book = Book.objects.create(
            name="KSIĘGA GŁÓWNA",
            description="Automatycznie utworzona księga główna.",
            user=request.user
        )

        # Tworzenie kont w "KSIĘDZE GŁÓWNEJ"
        accounts_data = [
            # Aktywa trwałe
            {"name": "Środki trwałe", "description": "Konto przeznaczone do ewidencji wartości trwałych, takich jak nieruchomości czy maszyny.", "account_type": "assets", "account_subtype": "fixed", "book": main_book},
            {"name": "Inwestycje długoterminowe", "description": "Konto do rejestrowania inwestycji, które mają być utrzymywane przez dłuższy czas, np. akcje.", "account_type": "assets", "account_subtype": "fixed", "book": main_book},
            {"name": "Lokaty", "description": "Konto do przechowywania środków ulokowanych na długoterminowych lokatach bankowych.", "account_type": "assets", "account_subtype": "fixed", "book": main_book},

            # Aktywa obrotowe
            {"name": "Zapasy", "description": "Konto do ewidencji zapasów, takich jak surowce czy produkty gotowe.", "account_type": "assets", "account_subtype": "current", "book": main_book},
            {"name": "Należności", "description": "Konto do rejestrowania kwot należnych od klientów lub kontrahentów.", "account_type": "assets", "account_subtype": "current", "book": main_book},
            {"name": "Środki pieniężne", "description": "Konto do ewidencji gotówki i środków na rachunkach bankowych.", "account_type": "assets", "account_subtype": "current", "book": main_book},

            # Środki pieniężne
            {"name": "Gotówka", "description": "Konto do przechowywania gotówki w kasie.", "account_type": "assets", "account_subtype": "cash", "book": main_book},
            {"name": "Rachunek bankowy", "description": "Konto do ewidencji środków przechowywanych na rachunkach bankowych.", "account_type": "assets", "account_subtype": "cash", "book": main_book},
            {"name": "Kryptowaluty", "description": "Konto do rejestrowania wartości posiadanych kryptowalut.", "account_type": "assets", "account_subtype": "cash", "book": main_book},

            # Zapasy
            {"name": "Towary", "description": "Konto do ewidencji towarów przeznaczonych do sprzedaży.", "account_type": "assets", "account_subtype": "inventory", "book": main_book},
            {"name": "Materiały", "description": "Konto do rejestrowania materiałów używanych w produkcji.", "account_type": "assets", "account_subtype": "inventory", "book": main_book},
            {"name": "Żywność", "description": "Konto do ewidencji zapasów żywności.", "account_type": "assets", "account_subtype": "inventory", "book": main_book},

            # Należności
            {"name": "Należności od znajomych", "description": "Konto do rejestrowania kwot pożyczonych znajomym.", "account_type": "assets", "account_subtype": "receivables", "book": main_book},
            {"name": "Należności z tytułu zwrotu podatków", "description": "Konto do ewidencji kwot należnych z tytułu zwrotu podatków.", "account_type": "assets", "account_subtype": "receivables", "book": main_book},
            {"name": "Należności od przedsiębiorstw", "description": "Konto do rejestrowania kwot należnych od firm.", "account_type": "assets", "account_subtype": "receivables", "book": main_book},

            # Koszty
            {"name": "Koszty rozwojowe", "description": "Konto do ewidencji wydatków na rozwój firmy.", "account_type": "expenses", "book": main_book},
            {"name": "Koszty zdrowotne", "description": "Konto do rejestrowania wydatków na opiekę zdrowotną.", "account_type": "expenses", "book": main_book},
            {"name": "Koszty żywienia", "description": "Konto do ewidencji wydatków na żywność.", "account_type": "expenses", "book": main_book},
            {"name": "Koszty transportu", "description": "Konto do rejestrowania wydatków na transport.", "account_type": "expenses", "book": main_book},
            {"name": "Koszty mieszkania", "description": "Konto do ewidencji wydatków na mieszkanie.", "account_type": "expenses", "book": main_book},

            # Zobowiązania krótkoterminowe
            {"name": "Zobowiązania wobec znajomych", "description": "Konto do rejestrowania kwot należnych znajomym.", "account_type": "liabilities", "account_subtype": "short_term", "book": main_book},
            {"name": "Zobowiązania wobec firm", "description": "Konto do ewidencji kwot należnych firmom.", "account_type": "liabilities", "account_subtype": "short_term", "book": main_book},
            {"name": "Zobowiązania wobec Skarbu Państwa", "description": "Konto do rejestrowania zobowiązań podatkowych.", "account_type": "liabilities", "account_subtype": "short_term", "book": main_book},

            # Zobowiązania długoterminowe
            {"name": "Kredyty", "description": "Konto do ewidencji długoterminowych kredytów.", "account_type": "liabilities", "account_subtype": "long_term", "book": main_book},
            {"name": "Obligacje", "description": "Konto do rejestrowania zobowiązań z tytułu obligacji.", "account_type": "liabilities", "account_subtype": "long_term", "book": main_book},
            {"name": "Leasing", "description": "Konto do ewidencji zobowiązań leasingowych.", "account_type": "liabilities", "account_subtype": "long_term", "book": main_book},

            # Kapitał własny
            {"name": "Oszczędności", "description": "Konto do rejestrowania oszczędności właściciela.", "account_type": "equity", "book": main_book},
            {"name": "Kapitał wypracowany", "description": "Konto do ewidencji kapitału wypracowanego przez firmę.", "account_type": "equity", "book": main_book},
            {"name": "Wartość netto aktywów trwałych", "description": "Konto do rejestrowania wartości netto aktywów trwałych.", "account_type": "equity", "book": main_book},

            # Przychody
            {"name": "Wynagrodzenie z pracy", "description": "Konto do ewidencji przychodów z wynagrodzenia.", "account_type": "revenue", "book": main_book},
            {"name": "Dodatkowe źródła dochodu", "description": "Konto do rejestrowania przychodów z dodatkowych źródeł.", "account_type": "revenue", "book": main_book},
            {"name": "Dochody z inwestycji", "description": "Konto do ewidencji przychodów z inwestycji.", "account_type": "revenue", "book": main_book},
            {"name": "Oszczędności i lokaty", "description": "Konto do rejestrowania przychodów z oszczędności i lokat.", "account_type": "revenue", "book": main_book},
            {"name": "Świadczenia socjalne", "description": "Konto do ewidencji przychodów ze świadczeń socjalnych.", "account_type": "revenue", "book": main_book},
        ]

        # Tworzenie kont z przypisaniem użytkownika
        for account_data in accounts_data:
            print(account_data)
            Account.objects.create(user=request.user, **account_data)

    # Obliczenia dla dashboardu
    total_accounts = Account.objects.filter(user=request.user).count()
    total_transactions = Transaction.objects.filter(user=request.user).count()
    total_revenues = Transaction.objects.filter(user=request.user, credit_account__account_type='revenue').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Transaction.objects.filter(user=request.user, debit_account__account_type='expenses').aggregate(Sum('amount'))['amount__sum'] or 0
    net_profit = total_revenues - total_expenses
    total_assets = Account.objects.filter(user=request.user, account_type='assets').aggregate(Sum('initial_balance'))['initial_balance__sum'] or 0
    total_liabilities = Account.objects.filter(user=request.user, account_type='liabilities').aggregate(Sum('initial_balance'))['initial_balance__sum'] or 0

    context = {
        'total_accounts': total_accounts,
        'total_transactions': total_transactions,
        'total_revenues': total_revenues,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        "net_profit_positive": net_profit > 0,
    }
    return render(request, 'Accountancy/dashboard.html.jinja', context)
