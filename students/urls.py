from django.urls import path
from . import views

urlpatterns = [
    #path('register/', views.StudentRegistrationView.as_view(), name='student_registration'),
    path('register/', views.register, name='student_registration'),
    path('profile/', views.student_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('enroll-unit/', views.StudentEnrollUnitView.as_view(), name='student_enroll_unit'),
    path('enrolled/', views.StudentUnitsListView.as_view(), name='view_enrolled_units'),
]