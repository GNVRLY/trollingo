from django.core.management.base import BaseCommand
from learning.models import Course, Lesson, Question, Answer


class Command(BaseCommand):
    help = "Ładuje przykładowe dane do Trollingo (kurs, lekcje, treść, pytania, odpowiedzi)."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Usuwam stare dane demo"))
        Answer.objects.all().delete()
        Question.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Tworzę kurs"))

        course = Course.objects.create(
            name="Angielski – podstawy",
            description="Podstawowy kurs angielskiego: słówka, zwroty i proste zdania. PL → EN.",
        )

        lesson_data = [
            # ===================== A1 =====================
            {
                "title": "Podstawowe rzeczowniki",
                "order": 1,
                "level": Lesson.Level.A1,
                "content": (
                    "Słówka:\n"
                    "- kot = cat\n"
                    "- pies = dog\n"
                    "- dom = house\n"
                    "- auto = car\n"
                    "- książka = book\n"
                    "\n"
                    "Przykłady:\n"
                    "- I have a cat.\n"
                    "- This is my house.\n"
                ),
                "questions": [
                    ("kot", "cat", ["dog", "mouse", "frog"]),
                    ("pies", "dog", ["cat", "bird", "cow"]),
                    ("dom", "house", ["flat", "car", "tree"]),
                    ("auto", "car", ["bike", "bus", "train"]),
                    ("książka", "book", ["notebook", "pen", "paper"]),
                ],
            },
            {
                "title": "Podstawowe czasowniki",
                "order": 2,
                "level": Lesson.Level.A1,
                "content": (
                    "Słówka:\n"
                    "- jeść = eat\n"
                    "- pić = drink\n"
                    "- spać = sleep\n"
                    "- iść = walk\n"
                    "- biegać = run\n"
                    "\n"
                    "Przykłady:\n"
                    "- I eat breakfast.\n"
                    "- We drink water.\n"
                ),
                "questions": [
                    ("jeść", "eat", ["sleep", "run", "sit"]),
                    ("pić", "drink", ["eat", "swim", "drive"]),
                    ("spać", "sleep", ["run", "work", "eat"]),
                    ("iść", "walk", ["run", "fly", "drink"]),
                    ("biegać", "run", ["walk", "jump", "sleep"]),
                ],
            },
            {
                "title": "Kolory i liczby",
                "order": 3,
                "level": Lesson.Level.A1,
                "content": (
                    "Kolory:\n"
                    "- czerwony = red\n"
                    "- niebieski = blue\n"
                    "- zielony = green\n"
                    "- czarny = black\n"
                    "- biały = white\n"
                    "\n"
                    "Liczby:\n"
                    "- jeden = one\n"
                    "- dwa = two\n"
                    "- trzy = three\n"
                ),
                "questions": [
                    ("czerwony", "red", ["blue", "green", "black"]),
                    ("niebieski", "blue", ["red", "yellow", "white"]),
                    ("zielony", "green", ["orange", "black", "pink"]),
                    ("jeden", "one", ["two", "three", "ten"]),
                    ("trzy", "three", ["one", "two", "four"]),
                ],
            },

            # ===================== A2 =====================
            {
                "title": "Przywitania i zwroty grzecznościowe",
                "order": 1,
                "level": Lesson.Level.A2,
                "content": (
                    "Zwroty:\n"
                    "- cześć = hi / hello\n"
                    "- dzień dobry = good morning / good afternoon\n"
                    "- dobranoc = good night\n"
                    "- dziękuję = thank you\n"
                    "- proszę = please\n"
                    "- przepraszam = sorry\n"
                    "\n"
                    "Przykłady:\n"
                    "- Hello! How are you?\n"
                    "- Thank you! You're welcome.\n"
                ),
                "questions": [
                    ("cześć", "hi", ["bye", "thanks", "sorry"]),
                    ("dzień dobry", "good morning", ["good night", "hello", "see you"]),
                    ("dziękuję", "thank you", ["please", "sorry", "welcome"]),
                    ("proszę", "please", ["thanks", "sorry", "hi"]),
                    ("przepraszam", "sorry", ["please", "hello", "goodbye"]),
                ],
            },
            {
                "title": "Rodzina",
                "order": 2,
                "level": Lesson.Level.A2,
                "content": (
                    "Rodzina:\n"
                    "- matka = mother\n"
                    "- ojciec = father\n"
                    "- siostra = sister\n"
                    "- brat = brother\n"
                    "- babcia = grandmother\n"
                    "- dziadek = grandfather\n"
                    "\n"
                    "Przykłady:\n"
                    "- My mother is kind.\n"
                    "- I have a brother.\n"
                ),
                "questions": [
                    ("matka", "mother", ["father", "sister", "brother"]),
                    ("ojciec", "father", ["mother", "grandfather", "uncle"]),
                    ("siostra", "sister", ["brother", "cousin", "aunt"]),
                    ("brat", "brother", ["sister", "father", "mother"]),
                    ("babcia", "grandmother", ["grandfather", "aunt", "cousin"]),
                ],
            },
            {
                "title": "Jedzenie i zakupy",
                "order": 3,
                "level": Lesson.Level.A2,
                "content": (
                    "Słówka:\n"
                    "- chleb = bread\n"
                    "- mleko = milk\n"
                    "- woda = water\n"
                    "- jabłko = apple\n"
                    "- cena = price\n"
                    "\n"
                    "Zwroty:\n"
                    "- Ile to kosztuje? = How much is it?\n"
                    "- Poproszę... = I'd like...\n"
                ),
                "questions": [
                    ("chleb", "bread", ["butter", "cheese", "meat"]),
                    ("mleko", "milk", ["water", "juice", "tea"]),
                    ("jabłko", "apple", ["banana", "orange", "grape"]),
                    ("cena", "price", ["store", "shop", "cash"]),
                    ("Ile to kosztuje?", "How much is it?", ["Where is it?", "What time is it?", "Who is it?"]),
                ],
            },

            # ===================== B1 =====================
            {
                "title": "Czas przeszły (Past Simple) – podstawy",
                "order": 1,
                "level": Lesson.Level.B1,
                "content": (
                    "Past Simple – regularne czasowniki:\n"
                    "- work → worked\n"
                    "- play → played\n"
                    "- watch → watched\n"
                    "\n"
                    "Przykłady:\n"
                    "- I worked yesterday.\n"
                    "- She played football.\n"
                ),
                "questions": [
                    ("pracowałem", "worked", ["work", "working", "worker"]),
                    ("grałem", "played", ["play", "playing", "player"]),
                    ("oglądałem", "watched", ["watch", "watching", "watches"]),
                    ("wczoraj", "yesterday", ["tomorrow", "today", "morning"]),
                    ("tydzień temu", "a week ago", ["next week", "last week", "in a week"]),
                ],
            },
            {
                "title": "Czasowniki nieregularne – top 5",
                "order": 2,
                "level": Lesson.Level.B1,
                "content": (
                    "Nieregularne:\n"
                    "- go → went\n"
                    "- have → had\n"
                    "- do → did\n"
                    "- see → saw\n"
                    "- take → took\n"
                    "\n"
                    "Przykłady:\n"
                    "- I went to school.\n"
                    "- We saw a movie.\n"
                ),
                "questions": [
                    ("iść (past)", "went", ["goed", "goes", "going"]),
                    ("mieć (past)", "had", ["haved", "has", "have"]),
                    ("robić (past)", "did", ["doed", "done", "does"]),
                    ("widzieć (past)", "saw", ["seed", "seen", "see"]),
                    ("brać (past)", "took", ["taked", "taken", "take"]),
                ],
            },
        ]

        for lesson_info in lesson_data:
            lesson = Lesson.objects.create(
                course=course,
                title=lesson_info["title"],
                order=lesson_info["order"],
                level=lesson_info["level"],
                content=lesson_info.get("content", ""),  # 👈 treść lekcji
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
        self.stdout.write("Odpal: / (kursy) → course → lesson → Start quiz")
