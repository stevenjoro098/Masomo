from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView
from .forms import UnitEnrollForm, RegistrationForm
from courses.models import Unit

# Create your views here.

'''class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password1'])
        login(self.request, user)
        return result'''


def register(request):
    """function based registration"""
    if request.method == 'POST':  # if posted data
        form = RegistrationForm(request.POST)  # receive forms posted data
        if form.is_valid():  # validate form posted data.
            form.save()  # save user info to db.
            return HttpResponseRedirect(reverse_lazy('login'))  # render login form for new user.
    else:
        form = RegistrationForm()  # render empty registration form.
    return render(request, 'students/student/registration.html', {'form': form})  # render to registration template.


class StudentEnrollUnitView(LoginRequiredMixin, FormView):
    """
    FormView displays a form. On error displays the form with validation error; on success, redirects to a new url..
    LoginRequired: User must be logged in.
        """
    unit = None
    form_class = UnitEnrollForm  # form to be rendered.
    template_name = 'courses/list/unit_detail.html'  # path to template/templates name.

    def form_valid(self, form):
        """Override method to add user to enrolled field."""
        self.unit = form.cleaned_data['unit']
        self.unit.students.add(self.request.user)  # add user to students field
        return super().form_valid(form)

    def get_success_url(self):
        """On successful redirect to user enrolled units list"""
        return reverse_lazy('view_enrolled_units')


class StudentUnitsListView(ListView):
    """List View class; enrolled units """
    model = Unit  # define model
    template_name = 'students/student/enrolled_units.html'  # path to template

    def get_queryset(self):
        """Override queryset to fetch only units enrolled by user"""
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])  # django lookup


def student_profile(request):
    """User to view Profile"""
    return render(request, 'students/student/profile.html')
