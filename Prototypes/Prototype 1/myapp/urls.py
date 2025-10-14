from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),            
    path('books/', views.books, name='books'),   
    path('books/', views.book_list, name='book_list'), 
    path('login/', views.login_view, name='login'),   
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'), 
    path('books/<int:pk>/borrow/', views.borrow_book, name='book-borrow'),
    path('borrows/<int:pk>/return/', views.return_book, name='book-return'),
    path('my-borrows/', views.MyBorrowsView.as_view(), name='my-borrows'),

]

