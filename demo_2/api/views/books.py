from django.shortcuts import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Book
from api.models import Author
from api.utils.serializers import BookSerializers


class Bookview(APIView):

    def get(self, request):
        book_obj = Book.objects.all()
        ret = BookSerializers(book_obj, many=True)
        print(ret.data)
        return Response(ret.data)

    def post(self, request):
        vaildata = BookSerializers(data=request.data)
        if vaildata.is_valid():
            book = vaildata.save()
            return Response(vaildata.data)
        else:
            return Response(vaildata.errors)


def test(request):
    a = Book
    print(a.objects.all())

    return HttpResponse("ok")