from django.shortcuts import render, redirect, HttpResponse
from apps.login_registration_app.models import User
from .models import Book
from django.contrib import messages


def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id=request.session['user_id'])[0]
    likes = Book.users_who_like.through.objects.all()
    context = {
        'this_user': this_user,
        'all_books': Book.objects.all(),
        'likes': Book.users_who_like.through.objects.all()
    }
    return render(request, 'home.html', context)


def create_book(request):
    if 'user_id' not in request.session and request.method != 'POST':
        # TODO: add message after validation is running
        # messages.error(request, "You must log in to view this content.")
        return redirect('/')
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request.value)
        return redirect('/books')
    this_user = User.objects.filter(id=request.session['user_id'])[0]
    new_book = Book.objects.create(
        title=request.POST['title'],
        desc=request.POST['desc'],
        uploaded_by=this_user)
    return redirect('/books')


def show_book(request, book_id):
    if 'user_id' not in request.session:
        # TODO: messages.error(request, "You must log in to view this content.")
        return redirect('/')
    this_user = User.objects.filter(id=request.session['user_id'])[0]
    this_book = Book.objects.filter(id=book_id)[0]
    context = {
        'this_book': this_book,
        'this_user': this_user,
    }
    if this_user.id == this_book.uploaded_by.id:
        return render(request, 'edit_book.html', context)
    return render(request, 'show_book.html', context)


def edit_book(request, book_id):
    if 'user_id' not in request.session and request.method != 'POST':
        # TODO: messages.error(request, "You must log in to view this content.")
        return redirect('/')
    this_book = Book.objects.filter(id=book_id)[0]
    this_book.title = request.POST['title']
    this_book.desc = request.POST['desc']
    this_book.save()
    return redirect(f'/books/')


def delete_book(request, book_id):
    if 'user_id' not in request.session and request.method != 'POST':
        # TODO: messages.error(request, "You must log in to view this content.")
        return redirect('/')
    this_book = Book.objects.filter(id=book_id)[0]
    this_book.delete()
    return redirect('/books/')

# can remove by doing the opposite


def like_book(request, book_id):
    if 'user_id' not in request.session and request.method != 'POST':
        # TODO: messages.error(request, "You must log in to view this content.")
        return redirect('/')
    this_book = Book.objects.filter(id=book_id)[0]
    this_user = User.objects.filter(id=request.session['user_id'])[0]
    this_book.users_who_like.add(this_user)
    this_book.save()
    return redirect('/books')


def unlike_book(request, book_id):
    if 'user_id' not in request.session and request.method != 'POST':
        # TODO: messages.error(request, "You must log in to view this content.")
        return redirect('/')
    this_book = Book.objects.filter(id=book_id)[0]
    this_user = User.objects.filter(id=request.session['user_id'])[0]
    this_book.users_who_like.remove(this_user)
    this_book.save()
    return redirect('/books')


def logout(request):
    request.session.flush()
    return redirect('/')
