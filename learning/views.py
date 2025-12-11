from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Course, Lesson, Question, Answer, UserLessonProgress


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


def lesson_quiz(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    questions = lesson.questions.prefetch_related("answers")

    score = None
    total = questions.count()

    if request.method == "POST":
        correct = 0

        for question in questions:
            field_name = f"question_{question.id}"
            answer_id = request.POST.get(field_name)

            if not answer_id:
                continue

            try:
                selected = question.answers.get(id=answer_id)
            except Answer.DoesNotExist:
                continue

            if selected.is_correct:
                correct += 1

        score = correct

        if request.user.is_authenticated:
            UserLessonProgress.objects.update_or_create(
                user=request.user,
                lesson=lesson,
                defaults={"score": score},
            )

    context = {
        "lesson": lesson,
        "questions": questions,
        "score": score,
        "total": total,
    }
    return render(request, "learning/lesson_quiz.html", context)
