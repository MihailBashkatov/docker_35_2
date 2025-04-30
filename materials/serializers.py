from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [LinkValidator(field=["url_link"])]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    @staticmethod
    def get_lessons_count(course):
        """Getting amount of lessons per course"""
        return course.lessons.all().count()

    @staticmethod
    def get_subscription(course):
        """Getting status of subscription"""
        if course.course_subscription.first():
            return course.course_subscription.first().subscription

    class Meta:
        model = Course
        fields = ["id", "name", "owner", "description", "subscription", "lessons_count", "lessons"]
