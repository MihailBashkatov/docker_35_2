from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self) -> None:
        self.owner = User.objects.create(email="user@user.com")
        self.course = Course.objects.create(
            name="test_course", description="test_course_description", owner=self.owner
        )

        self.lesson = Lesson.objects.create(
            name="test_lesson",
            description="test_lesson_description",
            course=self.course,
            owner=self.owner,
        )

        self.client.force_authenticate(user=self.owner)

    def test_course_retrieve(self):
        url = reverse("materials:courses-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "test_course")

    def test_course_create(self):
        url = reverse("materials:courses-list")
        data = {"name": "Second Test", "description": "description_second_test"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        url = reverse("materials:courses-detail", args=(self.course.pk,))
        data = {"name": "Guitar"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Guitar")

    def test_course_delete(self):
        url = reverse("materials:courses-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse("materials:courses-list")
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "name": self.course.name,
                "owner": self.owner.pk,
                "subscription": None,
                "lessons_count": 1,
                "lessons": [
                    {
                        "id": self.lesson.pk,
                        "name": self.lesson.name,
                        "description": self.lesson.description,
                        "preview": None,
                        "url_link": None,
                        "course": self.course.pk,
                        "owner": self.owner.pk,
                    }
                ],
            }
        ]

        self.assertEqual(Course.objects.all().count(), 1)

        self.assertEqual(data, result)


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.owner = User.objects.create(email="user@user.com")
        self.course = Course.objects.create(
            name="test_course", description="test_course_description", owner=self.owner
        )

        self.lesson = Lesson.objects.create(
            name="test_lesson",
            description="test_lesson_description",
            course=self.course,
            owner=self.owner,
        )

        self.client.force_authenticate(user=self.owner)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson-detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "test_lesson")

    def test_lesson_create(self):
        url = reverse("materials:lesson-create")
        data = {
            "name": "Second Test",
            "description": "description_second_test",
            "course": self.course.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {"name": "New Lesson"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "New Lesson")

    def test_lesson_delete(self):
        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lesson-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": None,
                    "url_link": None,
                    "course": self.course.pk,
                    "owner": self.owner.pk,
                }
            ],
        }

        self.assertEqual(Lesson.objects.all().count(), 1)

        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email="user@user.com")
        self.course = Course.objects.create(
            name="test_course", description="test_course_description", owner=self.user
        )

        self.subscription = Subscription.objects.create(
            user=self.user, course=self.course, subscription=False
        )

        self.client.force_authenticate(user=self.user)

    def test_subscription_retrieve(self):
        url = reverse("materials:subscription")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0].get("subscription"), False)
