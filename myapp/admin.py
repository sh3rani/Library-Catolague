from django.contrib import admin
from .models import Book, Reservation, IssuedBook, User
from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_superuser  

class bookAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'book_title', 'book_category', 'book_img', 'book_total_copies')
    search_fields = ('book_id', 'book_title', 'book_author')
    list_filter = ('book_title', 'book_category')  

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'role')
    search_fields = ('user_id', 'username', 'role')
    ordering = ('user_id', 'username')

class ReservationAdmin(admin.ModelAdmin):
    list_display =('book','user_id','date_reserved','date_redeem', 'status')
    search_fields = ('book','user_id')
    list_filter = ('book','status')


class IssuedBookAdmin(admin.ModelAdmin) :
    list_display =('book','user_id','issue_date','return_date','available')
    search_fields = ('book','user_id')
    list_filter = ('book','issue_date')


admin.site.register(Book, BookAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(IssuedBook, IssuedBookAdmin)
admin.site.register(Reservation, ReservationAdmin)

