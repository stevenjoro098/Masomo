from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/<pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('units/<id>/', views.UnitsView.as_view(), name='courses_units_list'),
    path('units/<pk>/enroll/', views.UnitEnrollView.as_view(), name='enroll'),
    path('enrolled/', views.MyUnitsView.as_view(), name='view_my_units'),
    path('register/', views.UserCreate.as_view(), name='register'),
    path('topics/<unit_id>', views.TopicsListView.as_view(), name='view_topics'),
    path('content/<topic_id>', views.ContentView.as_view(), name='contents'),
]