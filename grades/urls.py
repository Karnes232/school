from django.urls import path
from django.contrib.auth import views as auth_views
from .views import PasswordsChangeView

from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('password/', PasswordsChangeView.as_view(template_name='grades/change-password.html'), name="password"),
    path("password_success", views.password_success, name="password_success"),
    path("create_course", views.create_course, name="create_course"),
    path("courses", views.courses, name="courses"),
    path("course/<int:course_id>", views.course, name="course"),
    path("student/<int:student_id>", views.student, name="student"),
    path("grades", views.grades, name="grades"),
    path("report", views.report, name="report"),
    path("report_all", views.report_all, name="report_all"),
    path("report_all/<int:student_id>", views.individual, name="individual"),
    path("course_report", views.course_report, name="course_report"),
    path(r'^export/xls/$', views.export_users_xls, name='export_users_xls'),
    path(r'^export/xls2/$', views.export_users_xls2, name='export_users_xls2'),

]
