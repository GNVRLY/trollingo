from django.urls import path
from . import views

app_name = "learning"

urlpatterns = [
    path("", views.CourseListView.as_view(), name="course_list"),
    path("course/<int:pk>/", views.CourseDetailView.as_view(), name="course_detail"),
    path("lesson/<int:pk>/", views.LessonDetailView.as_view(), name="lesson_detail"),
    path("lesson/<int:pk>/quiz/", views.lesson_quiz, name="lesson_quiz"),
]
