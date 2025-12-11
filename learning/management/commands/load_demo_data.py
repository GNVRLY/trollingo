from django.core.management.base import BaseCommand
from learning.models import Course, Lesson, Question, Answer


class Command(BaseCommand):
    help = "Ładuje przykładowe dane do Trollingo (kurs, lekcje, pytania, odpowiedzi)."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Usuwam stare dane demo"))
        Answer.objects.all().delete()
        Question.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Tworzę kurs"))

        course = Course.objects.create(
            name="Angielski – podstawy",
            description="Podstawowy kurs angielskiego: słówka i proste wyrażenia.",
        )

        lesson_data = [
            {
                "title": "Podstawowe rzeczowniki",
                "order": 1,
                "level": Lesson.Level.A1,
                "questions": [
                    ("kot", "cat", ["dog", "mouse", "frog"]),
                    ("pies", "dog", ["cat", "bird", "cow"]),
                    ("dom", "house", ["flat", "car", "tree"]),
                ],
            },
            {
                "title": "Podstawowe czasowniki",
                "order": 2,
                "level": Lesson.Level.A1,
                "questions": [
                    ("jeść", "eat", ["sleep", "run", "sit"]),
                    ("pić", "drink", ["eat", "swim", "drive"]),
                    ("biegać", "run", ["walk", "jump", "sleep"]),
                ],
            },
            {
                "title": "Przywitania i zwroty grzecznościowe",
                "order": 3,
                "level": Lesson.Level.A2,
                "questions": [
                    ("cześć", "hi", ["bye", "thanks", "sorry"]),
                    ("dzień dobry", "good morning", ["good night", "hello", "see you"]),
                    ("dziękuję", "thank you", ["please", "sorry", "welcome"]),
                ],
            },
            {
                "title": "Rodzina",
                "order": 4,
                "level": Lesson.Level.A2,
                "questions": [
                    ("matka", "mother", ["father", "sister", "brother"]),
                    ("ojciec", "father", ["mother", "grandfather", "uncle"]),
                    ("siostra", "sister", ["brother", "cousin", "aunt"]),
                ],
            },
        ]

        for lesson_info in lesson_data:
            lesson = Lesson.objects.create(
                course=course,
                title=lesson_info["title"],
                order=lesson_info["order"],
                level=lesson_info["level"],
            )
            self.stdout.write(f"  - Lekcja: {lesson.title} ({lesson.level})")

            for polish, correct_en, wrong_answers in lesson_info["questions"]:
                q = Question.objects.create(
                    lesson=lesson,
                    text=f"Jak po angielsku będzie: '{polish}'?",
                )

                Answer.objects.create(
                    question=q,
                    text=correct_en,
                    is_correct=True,
                )

                for wrong in wrong_answers:
                    Answer.objects.create(
                        question=q,
                        text=wrong,
                        is_correct=False,
                    )

        self.stdout.write(self.style.SUCCESS("Dane demo zostały załadowane."))
