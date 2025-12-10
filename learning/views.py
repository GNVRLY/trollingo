from django.views.generic import ListView, DetailView

from .models import Course, Lesson


class CourseListView(ListView):
    model = Course
    template_name = "learning/course_list.html"
    context_object_name = "courses"


class CourseDetailView(DetailView):
    model = Course
    template_name = "learning/course_detail.html"
    context_object_name = "course"


class LessonDetailView(DetailView):
    model = Lesson
    template_name = "learning/lesson_detail.html"
    context_object_name = "lesson"
