from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from .models import Answer, Course, Lesson, UserLessonProgress

def home(request):
    if request.user.is_authenticated:
        return redirect("learning:course_list")
    return render(request, "learning/home.html")

class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "learning/course_list.html"
    context_object_name = "courses"
    login_url = "learning:login"


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "learning/course_detail.html"
    context_object_name = "course"
    login_url = "learning:login"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Zaloguj się, aby kontynuować.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        progresses = UserLessonProgress.objects.filter(
            user=self.request.user,
            lesson__course=self.object,
        )

        context["progress_map"] = {p.lesson_id: p for p in progresses}
        return context


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = "learning/lesson_detail.html"
    context_object_name = "lesson"
    login_url = "learning:login"


@login_required(login_url="learning:login")
def lesson_quiz(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    questions = lesson.questions.prefetch_related("answers")

    total = questions.count()
    XP_PER_POINT = 10

    all_lessons = list(
        Lesson.objects.filter(course=lesson.course).order_by("level", "order", "id")
    )
    idx = next((i for i, l in enumerate(all_lessons) if l.id == lesson.id), None)
    next_lesson = all_lessons[idx + 1] if idx is not None and idx + 1 < len(all_lessons) else None

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
        new_xp = score * XP_PER_POINT

        with transaction.atomic():
            existing = UserLessonProgress.objects.filter(user=request.user, lesson=lesson).first()
            old_score = existing.score if existing else 0
            old_xp = old_score * XP_PER_POINT

            UserLessonProgress.objects.update_or_create(
                user=request.user,
                lesson=lesson,
                defaults={"score": score},
            )

            profile = request.user.profile
            old_level = profile.level

            delta_xp = max(new_xp - old_xp, 0)
            profile.xp += delta_xp
            profile.save()

            new_level = profile.level
            level_up = new_level > old_level

        return render(
            request,
            "learning/lesson_quiz_result.html",
            {
                "lesson": lesson,
                "score": score,
                "total": total,
                "delta_xp": delta_xp,
                "next_lesson": next_lesson,
                "level_up": level_up,
                "new_level": new_level,
            },
        )

    return render(
        request,
        "learning/lesson_quiz.html",
        {
            "lesson": lesson,
            "questions": questions,
            "total": total,
        },
    )

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
    return redirect("learning:home")
