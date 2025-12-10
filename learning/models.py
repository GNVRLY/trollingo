from django.db import models
from django.conf import settings


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    class Level(models.TextChoices):
        A1 = "A1", "A1 – początkujący"
        A2 = "A2", "A2 – podstawowy"
        B1 = "B1", "B1 – średnio zaawansowany"
        B2 = "B2", "B2 – wyższy średnio"
        C1 = "C1", "C1 – zaawansowany"
        C2 = "C2", "C2 – biegły"

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=1)
    level = models.CharField(
        max_length=2,
        choices=Level.choices,
        default=Level.A1,
    )

    class Meta:
        ordering = ["level", "order"]

    def __str__(self):
        return f"{self.course.name} – {self.title} ({self.level})"



class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'OK' if self.is_correct else 'X'})"


class UserLessonProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "lesson")

    def __str__(self):
        return f"{self.user} – {self.lesson} – {self.score} pkt"

