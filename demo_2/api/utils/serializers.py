from rest_framework import serializers
from rest_framework.response import Response
from api.models import Book
from api.models import Author


class BookSerializers(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('title',
                  'price',
                  'pub_date',
                  'publish',
                  'authors',
                  )

    title = serializers.CharField(max_length=32)
    price = serializers.IntegerField()
    pub_date = serializers.DateField()
    publish_name = serializers.CharField(source="publish.name", read_only=True)
    publish = serializers.CharField(source="publish.id", write_only=True)
    authors = serializers.SerializerMethodField()
    authors_id = serializers.SerializerMethodField()

    def get_authors(self, obj):
        author_obj = Author.objects.all()
        return [i.name for i in author_obj]

    def get_authors_id(self, obj):
        author_obj = Author.objects.all()
        return [i.id for i in author_obj]

    def create(self, validated_data):
        print(validated_data)
        return Response(123)