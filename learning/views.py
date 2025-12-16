from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


from .models import Course, Lesson, Question, Answer, UserLessonProgress
class CourseListView(ListView):
    model = Course
    template_name = "learning/course_list.html"
    context_object_name = "courses"


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "learning/course_detail.html"
    context_object_name = "course"
    login_url = "learning:login"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(
                request,
                "Zaloguj się, aby kontynuować."
            )
        return super().dispatch(request, *args, **kwargs)


class LessonDetailView(DetailView):
    model = Lesson
    template_name = "learning/lesson_detail.html"
    context_object_name = "lesson"


@login_required
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

def register(request):
    if request.user.is_authenticated:
        return redirect("learning:course_list")

    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Konto utworzone. Jesteś zalogowany.")
        return redirect("learning:course_list")

    return render(request, "learning/register.html", {"form": form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("learning:course_list")

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, "Zalogowano.")
        return redirect("learning:course_list")

    return render(request, "learning/login.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.info(request, "Wylogowano.")
    return redirect("learning:course_list")

