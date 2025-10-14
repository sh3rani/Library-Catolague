from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Book(models.Model):
    book_id = models.CharField(max_length=100)
    book_title = models.CharField(max_length=100)
    book_img = models.ImageField(upload_to='books/',null=True, blank=True)
    book_author = models.CharField(max_length=50)
    book_total_copies = models.PositiveIntegerField(validators=[MinValueValidator(1) ,MaxValueValidator(100)])
    book_category = models.CharField(max_length=100)
    cover = models.ImageField(
    upload_to='book_covers/',
    blank=True,
    null=True,
    default='book_covers/default_cover.jpg'  
)


    def __str__(self): 
        return f"{self.book_title} by {self.book_author}"
    

class User(models.Model):
    user_id = models.CharField(primary_key=True) 
    user_Password = models.CharField(max_length=128)
    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.username 
    
class Reservation(models.Model):
    STATUS_CHOICES =[
        ('pending', 'Request Pending'),
        ('not returned', 'Not Returned by Previous User'),
    ]
    book =  models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date_reserved = models.DateTimeField(default=timezone.now)
    date_redeem = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='pending')

    def redeem(self):
        self.date_redeem = timezone.now()
        self.save()

    def is_redeemed(self):
        return self.date_redeem is not None

    def __str__(self):
        return f"Reservation for{self.book.book_title}  by {self.user_id.username}" 
    
class IssuedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=1 )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_date = models.DateField(default=timezone.now)
    return_date = models.DateField()
    available = models.BooleanField(default=True)

    def mark_returned(self):
        self.available = True
        self.save()

    def mark_issued(self):    
        self.available = False
        self.save()

    def is_overdue(self):
        return timezone.now().date()> self.return_date

    def __str__(self): 
        return f"IssuedBook(book={self.book.book_title},  user={self.user.username}, issue_date={self.issue_date}, return_date={self.return_date}, available={self.available})"


class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrows')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrows')
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_back = models.DateTimeField(null=True, blank=True)
    returned = models.BooleanField(default=False)

    class Meta:
        ordering = ['-borrowed_at']

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"

       