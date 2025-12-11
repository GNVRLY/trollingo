from django.contrib import admin
from .models import Course, Lesson, Question, Answer, UserLessonProgress


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "lesson")
    inlines = [AnswerInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "level", "order")
    list_filter = ("course", "level")
    ordering = ("course", "level", "order")


admin.site.register(Course)
admin.site.register(Answer)
admin.site.register(UserLessonProgress)
