from django.urls import path

from . import views

app_name = 'app'
urlpatterns = [
    path("", views.index, name="index"),
    path("add_item/", views.add_item, name="add_item"),
    path("login/", views.login, name="login"),
    path("registration/", views.register, name="registration"),
    path("register_method/", views.register_method, name="register_method"),
    path("login_method/", views.login_method, name="login_method"),
    path("logged_in/", views.logged_in, name="logged_in_page"),
    path("logout/", views.logged_out, name="logout"),
    path("to_do_list/", views.to_do_list, name="to do list"),
    path("completed/<int:id>/", views.completed, name="completed"),
    path("edit/<int:id>/", views.edit, name="edit"),
    path("update_item/<int:id>", views.edit_item, name="edit")
]