from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from ..models import Course, Unit, Topics, Content
from .serializers import CourseSerializer, UnitsSerializer, UserSerializer, TopicSerializer, ContentsSerializer


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class UnitsView(generics.ListAPIView):
    serializer_class = UnitsSerializer

    def get_queryset(self):
        courses = self.kwargs['id']
        return Unit.objects.filter(course=courses)


class MyUnitsView(generics.ListAPIView):
    serializer_class = UnitsSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # courses = self.kwargs['id']
        return Unit.objects.filter(students=self.request.user)


class UnitEnrollView(views.APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, format=None):
        unit = get_object_or_404(Unit, pk=pk)
        unit.students.add(request.user)
        return Response({'enrolled': True})


class TopicsListView(generics.ListAPIView):
    # authentication_classes = (BasicAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = TopicSerializer

    def get_queryset(self):
        # unit = self.kwargs['id']
        return Topics.objects.filter(unit=self.kwargs['unit_id'])


class ContentView(generics.ListAPIView):
    serializer_class = ContentsSerializer

    def get_queryset(self, **kwargs):
        try:
            topic = Topics.objects.get(id=self.kwargs['topic_id'])
            return topic.unit_contents.all()
        except:
            pass


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()

    permission_classes = (AllowAny,)

    def post(self, request, format='json'):
        data = request.data
        serializer_class = UserSerializer(data=data)
        if serializer_class.is_valid():
            password = serializer_class.validated_data.get('password')
            serializer_class.validated_data['password'] = make_password(password)
            new_user = serializer_class.save()
            if new_user:
                return Response(status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
