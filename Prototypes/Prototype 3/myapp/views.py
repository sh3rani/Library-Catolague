from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Book
from django.utils.decorators import method_decorator
from django.views import generic
from django.shortcuts import get_object_or_404
from .forms import RegisterForm
from .models import Borrow  
from django.utils import timezone
from datetime import timedelta


@login_required(login_url='login')
def home(request):
    books = Book.objects.all()
    return render(request, 'myapp/home.html', {'books': books})

@login_required(login_url='login')
def books(request):
    all_books = Book.objects.all()  
    return render(request, 'myapp/books.html', {'books': all_books})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "myapp/login.html")


def logout_view(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})


@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.available_copies < 1:
        messages.error(request, 'No copies available')
        return redirect(book.get_absolute_url())

    due = timezone.now() + timedelta(days=14) 
    Borrow.objects.create(user=request.user, book=book, due_back=due)
    book.available_copies -= 1
    book.save()

    messages.success(request, f'You borrowed "{book.title}" — due {due.date()}')
    return redirect('catalog:my-borrows')


@login_required
def return_book(request, pk):
    borrow = get_object_or_404(Borrow, pk=pk, user=request.user, returned=False)
    borrow.returned = True
    borrow.save()
    borrow.book.available_copies += 1
    borrow.book.save()

    messages.success(request, f'You returned "{borrow.book.title}"')
    return redirect('catalog:my-borrows')


@method_decorator(login_required, name='dispatch')
class MyBorrowsView(generic.ListView):
    model = Borrow
    template_name = 'catalog/my_borrows.html'
    paginate_by = 10

    def get_queryset(self):
        return Borrow.objects.filter(user=self.request.user, returned=False).select_related('book')

def book_list(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()
    
    return render(request, 'books.html', {'books': books})

