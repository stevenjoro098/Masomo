from django.db import models
from django.contrib.auth.models import User  # import user model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.template.loader import render_to_string
from django.utils.text import slugify


# Create your models here.
class Programme(models.Model):
    name = models.CharField(max_length=200, default='Programme')

    def __str__(self):
        return self.name


class Departments(models.Model):
    programme = models.ForeignKey(Programme, related_name='programme', on_delete=models.CASCADE)
    title = models.CharField(max_length=250, default='Department')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Course(models.Model):
    programme = models.ForeignKey(Programme, related_name='course_programme', on_delete=models.CASCADE)
    department = models.ForeignKey(Departments, related_name='department', on_delete=models.CASCADE)
    courses = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    overview = models.TextField()

    def __str__(self):
        return self.courses


class Semester(models.Model):
    course = models.ForeignKey(Course, related_name='course_year', on_delete=models.CASCADE)
    year = models.CharField(max_length=20)

    def __str__(self):
        return self.year


class Unit(models.Model):
    course = models.ForeignKey(Course, related_name='course', on_delete=models.CASCADE)
    year = models.ForeignKey(Semester, related_name='semester_units', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(User, related_name='units_created', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User, related_name='course_joined', blank=True)  # enroll students to UNIT

    # manytomany field i.e a single user can enroll to multiple UNITS and a single UNIT can have many enrolled students.

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        """ Override the save method in order to automatically slugify the Slug Field using the title field """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Topics(models.Model):
    unit = models.ForeignKey(Unit, related_name='related_topics', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='topic')
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Content(models.Model):
    topics = models.ForeignKey(Topics, related_name='unit_contents', on_delete=models.CASCADE)
    '''Contenttypes are Django's way of identifying database tables. 
    Every Database table is represented as a row in the content type table which is created and maintained 
    by Django. There are many operations and manipulations that you could do to a model using this Content Type module,'''
    '''Since we have a Database representation of tables in these Content Type table, what Django does is 
    use this to reference a table and then add an integer field to link to an id of that particular table, 
    thus accomplishing a relationship coz we now the table, and its id.'''

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': (
        'text',
        'video',
        'image',
        'file'
    )})
    # content_type is the reference to the content_type or the table used for the relation.
    object_id = models.PositiveIntegerField()  # The object_id is used to store the id of the row, or kind of like a foreign key (not a foreign key though!)
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True)  # the order is calculated with respect to the module field.

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}'


class ItemBase(models.Model):
    """ Model Inheritance:Useful when you want to put some common information into several models """
    owner = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string(
            f'courses/manage/content/{self._meta.model_name}.html',
            {'item': self}
        )


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    image = models.ImageField(upload_to='images/')


class Video(ItemBase):
    url = models.URLField()
