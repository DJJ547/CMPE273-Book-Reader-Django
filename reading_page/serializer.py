from rest_framework import serializers
from bson import ObjectId


class ObjectIdField(serializers.Field):

    def to_representation(self, value):
        return str(value)  # Convert ObjectId to string for JSON

    def to_internal_value(self, data):
        return ObjectId(data)  # Convert string back to ObjectId


class ChapterSerializer(serializers.Serializer):
    id = ObjectIdField(source='_id')  # Map `_id` to `id`
    book_id = serializers.IntegerField()
    book_name = serializers.CharField()
    author = serializers.CharField()
    chapter_number = serializers.IntegerField()
    chapter_title = serializers.CharField()
    chapter_content = serializers.ListField(child=serializers.CharField())  # List of strings
    book_cover = serializers.CharField()
