# Third-party
from rest_framework import serializers

# Mine
from app01.models import (
                          CourseCategory,
                          Course
                          )


class CourseCategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = CourseCategory

        fields = "__all__"


class CourseSerializers(serializers.ModelSerializer):

    class Meta:
        model = Course

        fields = (
            "pk",
            "name",
            "course_img",
            "course_type",
            "brief",
            "level",
            "pub_date",
            "period",
            "order",
            "attachment_path",
            "status",
            "category"
        )

        category = serializers.CharField(source="category.pk")
