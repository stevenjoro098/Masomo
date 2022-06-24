from django.apps import apps
from django.forms import modelform_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from .models import Unit, Topics, Content, Course
from .forms import TopicsFormSet
from students.forms import UnitEnrollForm
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.shortcuts import render

'''Function based Login method'''


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():  # Validate
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'],
                                password=cd['password'])
            if user is not None:  # If user exists
                if user.is_active:  # Active user
                    login(request, user)  # Allow user into the current session.
                    if user.groups.values_list('name', flat=True).first() == 'Instructors':  # Check if user is in the
                        # Instructors Group
                        return HttpResponseRedirect(reverse_lazy('units_list'))  # Redirect Instructor to Units he
                        # Created
                    else:
                        # Else redirect the users to the list of courses page.
                        return HttpResponseRedirect(reverse_lazy('list_courses'))
                else:
                    # Return an 'invalid login' error message.

                    return HttpResponse('Disabled Account')
        else:

            return HttpResponse('Invalid Login')
    else:
        # the login is a  GET request, so just show the user the login form.
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})  # render to html page the Form.


'''Create units Classed based view: 
        Inherits  Mixins: Login Required Mixin and CreateView Class
'''


class UnitCreateView(LoginRequiredMixin, CreateView):  # user must Login in order to create a Unit
    template_name = 'courses/manage/units/form.html'  # the path to form creation template.
    model = Unit  # Define the model
    fields = ['course', 'title', 'year', 'overview']  # Defined fields for the Unit create form.
    success_url = reverse_lazy('units_list')  # When successful redirect to units_list created by instructor.

    def form_valid(self, form):  # Override form validation method.
        form.instance.owner = self.request.user  # set owner field to logged user.
        return super().form_valid(form)


class UnitsListView(LoginRequiredMixin, ListView):
    """List all Units created by user"""
    template_name = 'courses/manage/units/course_list.html'  # path to list template
    model = Unit  # Define model
    context_object_name = 'units_list'  # override the default object name rendered in the template.

    def get_queryset(self):
        """Override the get_queryset method to fetch on Units created by the User."""
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)  # filter


class UnitsStudentsListView(ListView):  # list Units for courses
    """List all Units under a Course ID."""
    template_name = 'courses/list/units_list.html'  # path to list template
    model = Unit
    context_object_name = 'units_list'  # override the object name rendered in template.

    def get_queryset(self):
        """Override get queryset method to fetch Units with similar course ID"""
        qs = super().get_queryset()
        return qs.filter(course=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        """Additional course information to the template"""
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(id=self.kwargs['id'])  # get course object.
        return context  # return the context data


class UnitDetailView(DetailView):
    """View object details..."""
    model = Unit
    template_name = 'courses/list/unit_detail.html'  # path to template

    def get_context_data(self, **kwargs):
        """Additional enroll action to the template"""
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = UnitEnrollForm(initial={'unit': self.object})  # Enroll form provided with initial data
        '''item = self.get_object()
        if item.students.get(username=self.request.user):
            context['user_enrolled'] = False
        else:
            context['user_enrolled'] = False'''
        return context


class UnitsUpdateView(UpdateView):  # inherits from Update class.
    """Make changes to the created Unit. Receives ID or Slug of object"""
    model = Unit  # define model
    fields = ['course', 'title', 'year', 'overview']  # fields
    template_name = 'courses/manage/units/form.html'  # path to template
    success_url = reverse_lazy('units_list')  # redirect to units list created by instructor.


class UnitsDeleteView(DeleteView):
    """Delete object using ID or Slug provided in the url..."""
    model = Unit
    template_name = 'courses/manage/units/unit_confirm_delete.html'
    success_url = reverse_lazy('units_list')


class TopicsListView(ListView):
    """ fetch topics created under Unit"""
    model = Topics
    template_name = 'courses/manage/units/topics_list.html'  # manage templates.
    context_object_name = 'topics_list'

    def get_queryset(self):
        """filter topics with unit id provided at the url..."""
        return Topics.objects.filter(unit=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        """Get additional unit information and render to the template..."""
        context = super().get_context_data(**kwargs)
        context['unit'] = Unit.objects.get(id=self.kwargs['pk'])
        return context


class StudentTopicsView(ListView):
    """List Topics to Students under a Unit Id..."""
    model = Topics  # define model
    template_name = 'courses/list/topics_list.html'  # list/template path.
    context_object_name = 'unit_topics'  # override object name(customize).

    def get_queryset(self):
        """Override the get queryset method to get topics with similar Unit Id..."""
        return Topics.objects.filter(unit=self.kwargs['pk'])


class StudentTopicDetail(DetailView):
    """View the topic in detail view"""
    model = Topics  # define model
    template_name = 'courses/list/topic_detail.html'  # path to template.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get topic object
        topic = self.get_object()  # method under DetailView class(fetches object by id or slug).
        context['topic'] = topic.unit_contents.all()  # fetch all content related to topic.
        return context


class TopicsUpdateView(TemplateResponseMixin, View):
    """TemplateResponseMixin: render_to_response method."""
    """Creating multiple topics on a single page"""
    template_name = 'courses/manage/units/formset.html'  # path to template.
    unit = None  # empty topic

    def dispatch(self, request, pk):
        """The dispatch method takes in the request and ultimately returns the response.
        Normally, it returns a response by calling (IE dispatching to) another method like get.
        Think of it as a middleman between requests and responses.
        """
        self.unit = get_object_or_404(Unit, id=pk)  # fetch UNIT object
        print(self.unit)
        return super().dispatch(request, pk)

    def get_formset(self, data=None):
        """This method fetches the formset created in forms.py """
        # .instance means this formset is being used to create new instance of self.topic.
        return TopicsFormSet(instance=self.unit, data=data)  # empty data, new instance of topic created.

    def get(self, request, *args, **kwargs):
        """GET: Formset object and render to template..."""
        formset = self.get_formset()
        return self.render_to_response({'unit': self.unit,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        """ POST instructors data"""
        formset = self.get_formset(data=request.POST)  # fetch POST data
        if formset.is_valid():  # validate formset
            formset.save()  # save the data to models topics.
            return redirect('units_list')  # if successful redirect to units list.
        return self.render_to_response({'topic': self.topic,  # else
                                        'formset': formset})


class ContentCreateUpdateView(TemplateResponseMixin, View):
    """ Adding content to related topics...
        Inherits from TemplateResponseMixin
        and View"""
    topic = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'  # path to template.

    def get_model(self, model_name):
        """Gets certain model from certain app..."""
        if model_name in ['text', 'video', 'image', 'file']:  # ensure the model_name is in the list or return None.
            return apps.get_model(app_label='courses',
                                  model_name=model_name)  # return the required model from the App Courses.
        return None

    def get_form(self, model, *args, **kwargs):
        """You can create forms from a given model using the standalone function modelform_factory().
            Create content creation form based on model name..."""
        Form = modelform_factory(model, exclude=['owner', 'order', 'created', 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, topic_id, model_name, id=None):  # receives id, model name, topic_id from url.
        """Receives a request and returns a response"""
        self.topic = get_object_or_404(Topics, id=topic_id)  # fetch related content topic
        self.unit = self.topic.unit  # fetch related unit
        self.model = self.get_model(model_name)  # get model using get_model method defined earlier.
        if id:
            # get object from database, parameters: (Model, ID, owner)
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        print(topic_id, model_name, id)
        return super().dispatch(request, topic_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        """Instructor request GET form based on model type (i.e text, image, file, url) instance..."""
        form = self.get_form(self.model,
                             instance=self.obj)  # create form instance using get_form method defined earlier
        return self.render_to_response({'form': form,  # render form to template and object
                                        'object': self.obj})

    def post(self, request, topic_id, model_name, id=None):
        """Handling posted data: Content created data"""
        form = self.get_form(self.model,  # get the data
                             instance=self.obj,  #
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():  # validate form
            obj = form.save(commit=False)  # do not save to db yet.
            obj.owner = request.user  # set owner to user
            obj.save()  # save to db
            if not id:
                # create new content
                Content.objects.create(topics=self.topic,
                                       item=obj)  # adding content to the content type
            return redirect('list_topics', self.unit.id)
        return self.render_to_response({'form': form,
                                        'object': self.obj})


class CoursesListView(ListView):
    model = Course
    template_name = 'courses/list/course_list.html'
    context_object_name = 'courses_list'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/list/course_detail.html'
