# python
import json

# Django

# Third-party
from rest_framework.views import APIView
from rest_framework.response import Response

# Mine
from ..serializers.serializersClass import (
    CourseCategorySerializers,
    CourseSerializers
)
from app01.models import (
    CourseCategory,
    Course
)


class CourseList(APIView):
    def get(self, request):
        origin_data = Course.objects.all()
        serializer_data = CourseSerializers(origin_data, many=True)
        response_data = {}
        if serializer_data.data:
            response_data["data"] = serializer_data.data
            response_data["error_no"] = 0
        else:
            response_data["error_no"] = 1
        obj = Response(response_data)
        obj["Access-Control-Allow-Headers"] = "Content-Type"
        obj["Access-Control-Allow-Origin"] = "*"
        return obj


class CourseCategoryList(APIView):

    def get(self, request):
        origin_data = CourseCategory.objects.all()
        serializer_data = CourseCategorySerializers(origin_data, many=True)
        response_data = {}
        if serializer_data.data:
            response_data["data"] = serializer_data.data
            response_data["error_no"] = 0
        else:
            response_data["error_no"] = 1
        obj = Response(response_data)
        obj["Access-Control-Allow-Headers"] = "Content-Type"
        obj["Access-Control-Allow-Origin"] = "*"
        return obj


class CourseDetails(APIView):
    pass
