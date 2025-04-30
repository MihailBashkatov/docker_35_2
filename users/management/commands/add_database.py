from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from materials.models import Course, Lesson
from users.models import Payment, User
from users.utils import create_user


class Command(BaseCommand):
    help = "Add test payments to the database"

    def handle(self, *args, **kwargs):
        # Delete Data from database
        User.objects.all().delete()
        Course.objects.all().delete()
        Lesson.objects.all().delete()
        Group.objects.all().delete()

        create_user()  # Creating users in database

        user_1 = User.objects.get(email="user1@user.com")
        user_2 = User.objects.get(email="user2@user.com")
        user_3 = User.objects.get(email="user3@user.com")
        user_4 = User.objects.get(email="user4@user.com")
        user_5 = User.objects.get(email="user5@user.com")

        # Creating group Moderators
        moderators = Group.objects.create(name="Moderators")
        user_1.groups.add(moderators)

        paid_course_python, _ = Course.objects.get_or_create(
            name="Python", description="Python Description", owner=user_1
        )
        paid_course_sql, _ = Course.objects.get_or_create(
            name="SQL", description="SQL Description", owner=user_2
        )
        paid_course_eng, _ = Course.objects.get_or_create(
            name="English", description="English Description", owner=user_3
        )

        paid_lesson_1, _ = Lesson.objects.get_or_create(
            name="Test Lesson Python 1",
            description="1 Test Description lesson python",
            course=paid_course_python,
            owner=user_1,
        )

        paid_lesson_2, _ = Lesson.objects.get_or_create(
            name="Test Lesson Python 2",
            description="2 Test Description lesson python",
            course=paid_course_python,
            owner=user_1,
        )
        paid_lesson_3, _ = Lesson.objects.get_or_create(
            name="Test Lesson SQL 1",
            description="1 Test Description lesson SQL",
            course=paid_course_sql,
            owner=user_2,
        )

        paid_lesson_4, _ = Lesson.objects.get_or_create(
            name="Test Lesson SQL 2",
            description="2 Test Description lesson SQL",
            course=paid_course_sql,
            owner=user_2,
        )
        paid_lesson_5, _ = Lesson.objects.get_or_create(
            name="Test Lesson English 1",
            description="3 Test Description lesson english",
            course=paid_course_eng,
            owner=user_3,
        )

        paid_lesson_6, _ = Lesson.objects.get_or_create(
            name="Test Lesson Eng 3",
            description="3 Test Description lesson English",
            course=paid_course_eng,
            owner=user_3,
        )

        payments = [
            {
                "user": user_1,
                "payment_date": "2020-01-01",
                "payment_summ": 100.0,
                "payment_mode": Payment.CARD,
                "paid_course": paid_course_python,
                "paid_lesson": paid_lesson_1,
            },
            {
                "user": user_2,
                "payment_date": "2010-02-02",
                "payment_summ": 200.0,
                "payment_mode": Payment.CARD,
                "paid_course": paid_course_python,
                "paid_lesson": paid_lesson_2,
            },
            {
                "user": user_2,
                "payment_date": "2016-06-08",
                "payment_summ": 867.0,
                "payment_mode": Payment.CASH,
                "paid_course": paid_course_sql,
                "paid_lesson": paid_lesson_3,
            },
            {
                "user": user_3,
                "payment_date": "2011-04-20",
                "payment_summ": 2765.89,
                "payment_mode": Payment.CASH,
                "paid_course": paid_course_sql,
                "paid_lesson": paid_lesson_4,
            },
            {
                "user": user_4,
                "payment_date": "2018-11-16",
                "payment_summ": 156.70,
                "payment_mode": Payment.CASH,
                "paid_course": paid_course_python,
                "paid_lesson": paid_lesson_5,
            },
            {
                "user": user_4,
                "payment_date": "2015-07-07",
                "payment_summ": 2380.89,
                "payment_mode": Payment.CARD,
                "paid_course": paid_course_sql,
                "paid_lesson": paid_lesson_6,
            },
            {
                "user": user_5,
                "payment_date": "2014-02-08",
                "payment_summ": 235,
                "payment_mode": Payment.CARD,
                "paid_course": paid_course_sql,
                "paid_lesson": paid_lesson_6,
            },
        ]

        for payment_data in payments:
            Payment.objects.get_or_create(**payment_data)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully added {len(payments)} test payments")
        ),
