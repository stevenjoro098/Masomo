from django.urls import path
from . import views

urlpatterns = [
    path('create/unit', views.UnitCreateView.as_view(), name='create_unit'),
    path('list/my/units', views.UnitsListView.as_view(), name='units_list'),
    path('update/unit/<int:pk>/', views.UnitsUpdateView.as_view(), name='update_units'),
    path('delete/unit/<int:pk>', views.UnitsDeleteView.as_view(), name='delete_unit_view'),
    path('topic/<pk>', views.TopicsUpdateView.as_view(), name='topics_update'),
    path('list/topics/<pk>/', views.TopicsListView.as_view(), name='list_topics'),
    path('list/units/topics/<pk>', views.StudentTopicsView.as_view(),name='list_topics_view'),
    path('topic/detail/<pk>/', views.StudentTopicDetail.as_view(), name='topic_details'),
    path('topic/detail/<pk>/<topic_id>', views.StudentTopicDetail.as_view(), name='topic_details_topic_id'),
    path('unit/<int:topic_id>/topic/<model_name>/create/', views.ContentCreateUpdateView.as_view(),
         name='topic_content_create'),
    path('unit/<int:topic_id>/topic/<model_name>/<id>/', views.ContentCreateUpdateView.as_view(),
         name='topic_content_update'),

    path('', views.CoursesListView.as_view(), name='list_courses'),
    path('<slug>/', views.CourseDetailView.as_view(), name='course_details'),
    path('courses/units/<id>/', views.UnitsStudentsListView.as_view(), name='list_semester_units'),
    path('unit/details/<slug>/',views.UnitDetailView.as_view(), name='unit_detail_view'),
]