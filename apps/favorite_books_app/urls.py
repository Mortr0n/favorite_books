from django.urls import path
from . import views
urlpatterns = [
    path('', views.home),
    path('logout', views.logout),
    path('book/create', views.create_book),
    path('book/<int:book_id>/edit', views.edit_book),
    path('book/<int:book_id>', views.show_book),
    path('book/<int:book_id>/delete', views.delete_book),
    path('book/<int:book_id>/like', views.like_book),
    path('book/<int:book_id>/unlike', views.unlike_book),
]
