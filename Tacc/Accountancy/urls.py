"""
URL configuration for Tacc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path('books/', views.books, name='books'),
    path('book/create/', views.create_book, name='create_book'),
    path('book/<int:book_id>/details/', views.book_details, name='book_details'),
    path('book/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('book/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('accounts/', views.accounts, name='accounts'),
    path('account/create/', views.create_account, name='create_account'),
    path('account/<int:account_id>/details/', views.account_details, name='account_details'),
    path('account/<int:account_id>/edit/', views.edit_account, name='edit_account'),
    path('account/<int:account_id>/delete/', views.delete_account, name='delete_account'),
    path('categories/', views.categories, name='categories'),
    path('category/create/', views.create_category, name='create_category'),
    path('category/<int:category_id>/details/', views.category_details, name='category_details'),
    path('category/<int:category_id>/edit/', views.edit_category, name='edit_category'),
    path('category/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('transactions/', views.transactions, name='transactions'),
    path('transaction/create/', views.create_transaction, name='create_transaction'),
    path('transaction/<int:transaction_id>/details/', views.transaction_details, name='transaction_details'),
    path('transaction/<int:transaction_id>/edit/', views.edit_transaction, name='edit_transaction'),
    path('transaction/<int:transaction_id>/delete/', views.delete_transaction, name='delete_transaction'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)