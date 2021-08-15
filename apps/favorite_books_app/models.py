from django.db import models
from apps.login_registration_app.models import User

class Book_Manager(models.Manager):
    def book_validator(self, post_data):
        errors ={}
        if len(post_data['title']) < 1:
            errors['title'] = 'The book must have a title'
        if len(post_data['desc']) < 5:
            errors['desc'] = 'Description must be at least 5 characters long'
        return errors


class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    objects = Book_Manager()

