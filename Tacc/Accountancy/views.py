from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from MAIN.utils import messages
from .models import *
from .forms import *
from datetime import datetime, timedelta
from django.db.models import Sum
from decimal import Decimal





# Create your views here.
@login_required
def books(request):
    books = Book.objects.filter(user=request.user)  # Filtrowanie książek użytkownika
    # messages.info(request, 'test')
    return render(request, 'Accountancy/books/main.html.jinja', {'books': books})

@login_required
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user  # Przypisanie książki do użytkownika
            book.save()
            messages.success(request, 'Księga została pomyślnie utworzona.')
            return redirect('books')
        messages.error(request, 'Wystąpił błąd podczas tworzenia księgi. Sprawdź formularz.')
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
            messages.success(request, 'Księga została pomyślnie zaktualizowana.')
            return redirect('books')
        messages.error(request, 'Wystąpił błąd podczas aktualizacji księgi. Sprawdź formularz.')
    else:
        form = BookForm(instance=book)
    return render(request, 'Accountancy/books/edit.html.jinja', {'form': form, 'book': book})

@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)  # Sprawdzenie właściciela książki
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Księga została pomyślnie usunięta.')
        return redirect('books')
    return render(request, 'Accountancy/books/delete.html.jinja', {'book': book})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Account, Transaction

@login_required
def accounts(request):
    accounts = Account.objects.filter(user=request.user)
    data = []
    data_by_id = {}

    for account in accounts:
        current_balance = account.calculate_balance()
        debit_transactions = Transaction.objects.filter(debit_account=account).order_by('-date')[:3]
        credit_transactions = Transaction.objects.filter(credit_account=account).order_by('-date')[:3]

        # Zapisz pełne dane do listy i słownika
        account_data = {
            'account': account,
            'current_balance': current_balance,
            'debit_transactions': debit_transactions,
            'credit_transactions': credit_transactions,
        }
        data.append(account_data)
        data_by_id[account.id] = {
            'current_balance': current_balance,
            'debit_transactions': debit_transactions,
            'credit_transactions': credit_transactions,
        }

    context = {
        'accounts': accounts,
        'data': data,
        'data_by_id': data_by_id,
    }

    return render(request, 'Accountancy/accounts/main.html.jinja', context)

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, user=request.user)  # Przekazanie użytkownika do formularza
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user  # Przypisanie konta do użytkownika
            account.save()
            messages.success(request, 'Konto zostało pomyślnie utworzone.')
            return redirect('accounts')
        messages.error(request, 'Wystąpił błąd podczas tworzenia konta. Sprawdź formularz.')
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
            messages.success(request, 'Konto zostało pomyślnie zaktualizowane.')
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
def transactions(request):
    transactions = Transaction.objects.filter(user=request.user).select_related('category')

    transactions_with_colors = [
        {
            'transaction': transaction,
            'category_color': transaction.category.color if transaction.category else None
        }
        for transaction in transactions
    ]
    print(transactions_with_colors)
    return render(request, 'Accountancy/transactions/main.html.jinja', {
        'transactions_with_colors': transactions_with_colors, 'transactions': transactions
    })

@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)  # Przekazanie użytkownika do formularza
        print(form.data)
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
    print(user)
    budgets = Budgets.objects.filter(user=user).select_related('category')
    print(budgets)

    budgets_with_colors = [
        {
            'budget': budget,
            'category_color': budget.category.color if budget.category else '#cccccc'
        }
        for budget in budgets
    ]

    return render(request, 'Accountancy/budgets/main.html.jinja', {
        'budgets_with_colors': budgets_with_colors
    })

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

from django.db.models import Sum
from django.utils.timezone import make_aware

# @login_required
# def report_details(request, report_id):
#     # Pobranie raportu przypisanego do zalogowanego użytkownika
#     report = get_object_or_404(Report, id=report_id, user=request.user)

#     # Pobranie wybranej księgi
#     book = report.book

#     # Pobranie kont użytkownika dla danej księgi
#     accounts = Account.objects.filter(user=request.user, book=book)

#     # Pobranie transakcji w zadanym okresie (z uwzględnieniem księgi)
#     transactions = Transaction.objects.filter(
#         user=request.user,
#         credit_account__book=book,  # Uwzględnij tylko transakcje związane z księgą
#         debit_account__book=book,   # zarówno po stronie kredytu, jak i debetu
#         created_at__gte=report.start_date,  # Data transakcji >= start_date
#         created_at__lte=report.end_date     # Data transakcji <= end_date
#     )

#     # Obliczenia tylko dla transakcji w zadanym okresie
#     total_revenues = transactions.filter(
#         credit_account__account_type='revenue'
#     ).aggregate(Sum('amount'))['amount__sum'] or 0

#     total_expenses = transactions.filter(
#         debit_account__account_type='expenses'
#     ).aggregate(Sum('amount'))['amount__sum'] or 0

#     # Salda początkowe kont (niezależne od zakresu dat) - NIE używane w obliczeniach transakcji
#     total_assets = accounts.filter(
#         account_type='assets'
#     ).aggregate(Sum('initial_balance'))['initial_balance__sum'] or 0

#     total_liabilities = accounts.filter(
#         account_type='liabilities'
#     ).aggregate(Sum('initial_balance'))['initial_balance__sum'] or 0

#     # Dane wygenerowane przez metodę raportu
#     report_data = report.generate_report()

#     context = {
#         'report': report,
#         'report_data': report_data,
#         'total_assets': total_assets,
#         'total_liabilities': total_liabilities,
#         'total_revenues': total_revenues,
#         'total_expenses': total_expenses,
#     }


#     #DEBUG
#     print(transactions.count())
#     for transaction in transactions:
#         print(f"Transaction ID: {transaction.id}, Amount: {transaction.amount}, Date: {transaction.created_at}, Debit Account: {transaction.debit_account.name}, Credit Account: {transaction.credit_account.name}")
#     #DEBUG

#     return render(request, 'Accountancy/reports/details.html.jinja', context)
@login_required
def report_details(request, report_id):
    # Pobranie raportu przypisanego do zalogowanego użytkownika
    report = get_object_or_404(Report, id=report_id, user=request.user)

    # Przekazanie zakresu dat do metody generate_report
    report_data = report.generate_report()

    context = {
        'report': report,
        'report_data': report_data,
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
    # Pobranie kont z bazy danych
    assets = Account.objects.filter(account_type='assets')
    liabilities = Account.objects.filter(account_type='liabilities')
    revenues = Account.objects.filter(account_type='revenue')
    expenses = Account.objects.filter(account_type='expenses')
    equity = Account.objects.filter(account_type='equity')

    # Obliczenie sum sald
    total_assets = sum(account.calculate_balance() for account in assets)
    total_liabilities = sum(account.calculate_balance() for account in liabilities)
    total_revenues = sum(account.calculate_balance() for account in revenues)
    total_expenses = sum(account.calculate_balance() for account in expenses)
    total_equity = sum(account.calculate_balance() for account in equity)

    # Obliczenie zysku netto
    net_income = total_revenues - total_expenses

    # Wskaźniki rentowności
    ros = (net_income / total_revenues * 100) if total_revenues else 0
    roa = (net_income / total_assets * 100) if total_assets else 0
    roe = (net_income / total_equity * 100) if total_equity else 0

    # Wskaźniki płynności
    current_assets = sum(
        account.calculate_balance() 
        for account in assets 
        if account.account_subtype == 'current'
    )
    current_liabilities = sum(
        account.calculate_balance() 
        for account in liabilities 
        if account.account_subtype == 'current'
    )
    inventory = sum(
        account.calculate_balance()
        for account in assets
        if account.account_subtype == 'inventory'
    )

    current_ratio = current_assets / current_liabilities if current_liabilities else 0
    quick_ratio = (current_assets - inventory) / current_liabilities if current_liabilities else 0

    # Wskaźnik zadłużenia
    debt_ratio = (total_liabilities / total_assets * 100) if total_assets else 0

    context = {
        'ros': round(ros, 2),
        'roa': round(roa, 2),
        'roe': round(roe, 2),
        'current_ratio': round(current_ratio, 2),
        'quick_ratio': round(quick_ratio, 2),
        'debt_ratio': round(debt_ratio, 2),
        'net_income': net_income,
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'total_revenues': total_revenues,
        'total_expenses': total_expenses,
        'total_equity': total_equity,
    }

    return render(request, 'Accountancy/analysis/financial_analysis.html.jinja', context)

@login_required
def financial_forecast(request):
    data = {}
    user = User.objects.get(username=request.user)
    transactions = Transaction.objects.filter(user=user)

    income_transactions = transactions.filter(credit_account__account_type='revenue')
    expense_transactions = transactions.filter(debit_account__account_type='expenses')

    start_date = transactions.order_by('date').first().date if transactions.exists() else None
    end_date = datetime.now() + timedelta(days=365*10)  # Prognoza na 10 lat do przodu

    for date in [start_date, end_date]:
        if date and date.tzinfo is None:
            date = make_aware(date)
            data
    
    return render(request, 'Accountancy/forecast/financial_forecast.html.jinja', {})


# from django.db.models import Sum
# from datetime import datetime, timedelta
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from django.utils import timezone
# from django.http import JsonResponse
# from .models import Transaction, Account, Book

# @login_required
# # def financial_forecast(request):
#     user = request.user

#     # Get the current book
#     book = Book.objects.filter(user=user).first()
#     if not book:
#         return render(request, 'Accountancy/forecast/financial_forecast.html.jinja', {
#             'error': 'No book found for forecasting'
#         })

#     # Fixed configuration: 10 years forward, 6 years backward, monthly steps
#     forward_months = 120  # 10 years
#     backward_months = 72  # 6 years
#     step_days = 30
#     date_format = '%Y-%m'
#     today = timezone.now().date()

#     # Generate forecast dates
#     forecast_dates = [
#         (today + timedelta(days=i * step_days)).strftime(date_format)
#         for i in range(forward_months)
#     ]

#     # Generate historical dates
#     historical_dates = []
#     historical_revenues = []
#     historical_expenses = []
#     historical_assets = []
#     historical_liabilities = []

#     for i in range(backward_months, 0, -1):
#         historical_date = today - timedelta(days=i * step_days)
#         historical_dates.append(historical_date.strftime(date_format))
#         end_date = historical_date + timedelta(days=step_days)

#         # Historical revenues
#         rev = float(Transaction.objects.filter(
#             credit_account__account_type='revenue',
#             credit_account__book=book,
#             user=user,
#             date__date__gte=historical_date,
#             date__date__lt=end_date
#         ).aggregate(Sum('amount'))['amount__sum'] or 0)
#         historical_revenues.append(rev)

#         # Historical expenses
#         exp = float(Transaction.objects.filter(
#             debit_account__account_type='expenses',
#             debit_account__book=book,
#             user=user,
#             date__date__gte=historical_date,
#             date__date__lt=end_date
#         ).aggregate(Sum('amount'))['amount__sum'] or 0)
#         historical_expenses.append(exp)

#         # Historical assets
#         assets = float(Account.objects.filter(
#             account_type='assets',
#             book=book,
#             user=user
#         ).aggregate(Sum('initial_balance'))['initial_balance__sum'] or 0)
#         historical_assets.append(assets)

#         # Historical liabilities
#         liabilities = float(Account.objects.filter(
#             account_type='liabilities',
#             book=book,
#             user=user
#         ).aggregate(Sum('initial_balance'))['initial_balance__sum'] or 0)
#         historical_liabilities.append(liabilities)

#     # Averages for smoothing
#     avg_revenue = sum(historical_revenues) / len(historical_revenues) if historical_revenues else 0
#     avg_expense = sum(historical_expenses) / len(historical_expenses) if historical_expenses else 0
#     avg_assets = sum(historical_assets) / len(historical_assets) if historical_assets else 0
#     avg_liabilities = sum(historical_liabilities) / len(historical_liabilities) if historical_liabilities else 0

#     # Forecast using exponential smoothing
#     alpha = 0.6
#     revenues, expenses, assets, liabilities, cashflow, aggregate = [], [], [], [], [], []

#     prev_rev, prev_exp, prev_asset, prev_liab = avg_revenue, avg_expense, avg_assets, avg_liabilities

#     for _ in range(forward_months):
#         rev = alpha * prev_rev + (1 - alpha) * avg_revenue
#         exp = alpha * prev_exp + (1 - alpha) * avg_expense
#         asset = alpha * prev_asset + (1 - alpha) * avg_assets
#         liab = alpha * prev_liab + (1 - alpha) * avg_liabilities
#         profit = rev - exp
#         total = profit + asset - liab

#         revenues.append(round(rev, 2))
#         expenses.append(round(exp, 2))
#         assets.append(round(asset, 2))
#         liabilities.append(round(liab, 2))
#         cashflow.append(round(profit, 2))
#         aggregate.append(round(total, 2))

#         prev_rev, prev_exp, prev_asset, prev_liab = rev, exp, asset, liab

#     forecast_data = {
#         'historical_dates': historical_dates,
#         'dates': forecast_dates,
#         'historical_revenues': historical_revenues,
#         'historical_expenses': historical_expenses,
#         'historical_assets': historical_assets,
#         'historical_liabilities': historical_liabilities,
#         'revenues': revenues,
#         'expenses': expenses,
#         'assets': assets,
#         'liabilities': liabilities,
#         'cashflow': cashflow,
#         'aggregate': aggregate,
#         'time_range': 'decade',
#         'time_ranges': ['decade']
#     }

#     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#         return JsonResponse(forecast_data)
#     print('\n\n\n\n\n', forecast_data, '\n\n\n\n\n')
#     return render(request, 'Accountancy/forecast/financial_forecast.html.jinja', {
#         'forecast_data': forecast_data,
#         'book': book
#     })

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
    # Wczytanie wszystkich kont użytkownika
    user_accounts = Account.objects.filter(user=request.user)

    # Obliczenie sumy sald wg typu konta
    def sum_balance(account_type):
        return sum([account.calculate_balance() for account in user_accounts.filter(account_type=account_type)])

    total_assets = sum_balance('assets')
    total_liabilities = sum_balance('liabilities')
    total_revenues = sum_balance('revenue')
    total_expenses = sum_balance('expenses')
    net_profit = total_revenues - total_expenses

    context = {
        'total_accounts': user_accounts.count(),
        'total_transactions': Transaction.objects.filter(user=request.user).count(),
        'total_revenues': total_revenues,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
        'net_profit_positive': net_profit > 0,
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
    }

    # messages.success(request, 'Witamy w panelu głównym!')
    # messages.info(request, 'Aby rozpocząć, możesz edytować lub usuwać automatycznie utworzone konta w "KSIĘDZE GŁÓWNEJ".')
    # messages.warning(request, 'Pamiętaj, aby regularnie tworzyć raporty finansowe i analizować swoje finanse!')
    # messages.error(request, 'Jeśli napotkasz jakiekolwiek problemy, skontaktuj się z działem wsparcia!')
    return render(request, 'Accountancy/dashboard.html.jinja', context)
    # Przekierowanie do strony głównej po utworzeniu księgi i kont
    # # Obliczenia dla dashboardu
    # total_accounts = Account.objects.filter(user=request.user).count()
    # total_transactions = Transaction.objects.filter(user=request.user).count()
    # total_revenues = Transaction.objects.filter(user=request.user, credit_account__account_type='revenue').aggregate(Sum('amount'))['amount__sum'] or 0
    # total_expenses = Transaction.objects.filter(user=request.user, debit_account__account_type='expenses').aggregate(Sum('amount'))['amount__sum'] or 0
    # net_profit = total_revenues - total_expenses
    # total_assets = Account.objects.filter(user=request.user, account_type='assets').aggregate(Sum('initial_balance'))['initial_balance__sum'] or 0
    # total_liabilities = Account.objects.filter(user=request.user, account_type='liabilities').aggregate(Sum('initial_balance'))['initial_balance__sum'] or 0

    # context = {
    #     'total_accounts': total_accounts,
    #     'total_transactions': total_transactions,
    #     'total_revenues': total_revenues,
    #     'total_expenses': total_expenses,
    #     'net_profit': net_profit,
    #     'total_assets': total_assets,
    #     'total_liabilities': total_liabilities,
    #     "net_profit_positive": net_profit > 0,
    # }
    # return render(request, 'Accountancy/dashboard.html.jinja', context)



@login_required
def goals(request):
    user = User.objects.get(username=request.user)
    goals = Goal.objects.all().filter(user=user)
    return render(request, 'Accountancy/goals/main.html.jinja', {'goals': goals})

@login_required
def create_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('goals')
    else:
        form = GoalForm()
    return render(request, 'Accountancy/goals/create.html.jinja', {'form': form})  

@login_required
def goal_details(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    account = goal.account
    amount = account.calculate_balance() if account else 0.00

    return render(request, 'Accountancy/goals/details.html.jinja', {
        'goal': goal,
        'account': account,
        'amount': amount
    })

@login_required
def edit_goal(request, goal_id):
    goal = Goal.objects.get(id=goal_id)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('goals')
    else:
        form = GoalForm(instance=goal)
    return render(request, 'Accountancy/goals/edit.html.jinja', {'form': form, 'goal': goal})

@login_required
def delete_goal(request, goal_id):
    goal = Goal.objects.get(id=goal_id)
    if request.method == 'POST':
        goal.delete()
        return redirect('goals')
    return render(request, 'Accountancy/goals/delete.html.jinja', {'goal': goal})