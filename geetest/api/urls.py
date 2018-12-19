# Django
from django.urls import path, re_path

# Mine
from .views import (
                    courseViews,
                    login,
                    captchaCheck
                    )

urlpatterns = [
    path("courses/", courseViews.CourseList.as_view()),
    path("course_sub/category/list/", courseViews.CourseCategoryList.as_view()),
    path("captcha_check/", captchaCheck.CaptchaCheck.as_view()),
    path("login/", login.LoginView.as_view()),
    re_path(r"courses/\d+/details-introduce", courseViews.CourseDetails.as_view())
]
