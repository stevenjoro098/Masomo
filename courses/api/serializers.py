from rest_framework import serializers
from ..models import Course, Departments, Programme, Unit, Topics, Content, Text, Image, Video, File
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from generic_relations.relations import GenericRelatedField


class ProgrammeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programme
        fields = ['name']


class DepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ['title', 'slug']


class CourseSerializer(serializers.ModelSerializer):
    programme = ProgrammeSerializer(read_only=True)
    department = DepartmentsSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'programme', 'department', 'courses', 'slug', 'overview']


class UnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'course', 'year', 'title', 'overview']


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = ['id', 'unit', 'title', 'description']


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['title', 'content']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['title', 'image']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['title', 'url']


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['title', 'file']


class ContentsSerializer(serializers.ModelSerializer):
    topics = GenericRelatedField({
        Topics: TopicSerializer(),
    })
    item = GenericRelatedField({
        Text: TextSerializer(),
        Image: ImageSerializer(),
        Video: VideoSerializer(),
        File: FileSerializer()
    })

    class Meta:
        model = Content
        fields = ('topics', 'item')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            return User.objects.create_user(validated_data['username'], validated_data['email'],
                                            make_password(validated_data['password']))
