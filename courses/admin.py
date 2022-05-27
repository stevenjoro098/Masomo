from django.contrib import admin
from .models import Programme, Semester, Course, Unit, Topics, Content, Departments, Text, Image, File


# Register your models here.
# use admin decorator
@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['year']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['courses']
    search_fields = ['courses']
    prepopulated_fields = {'slug': ('courses',)}  # slugify courses


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'owner']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Topics)
class TopicsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Departments)
class DepartementsAdmin(admin.ModelAdmin):
    list_display = ['title']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['topics']


@admin.register(Text)
class TextsViewAdmin(admin.ModelAdmin):
    list_display = ['content']


@admin.register(Image)
class ImageViewAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']

@admin.register(File)
class FileViewAdmini(admin.ModelAdmin):
    list_display = ['title','file']