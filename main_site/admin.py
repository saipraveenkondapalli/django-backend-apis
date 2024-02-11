import random
import string

from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django_countries import countries

from .forms import BlogForm, BlogAddForm
from .models import (
    CompanyTrack,
    License,
    Api,
    Website,
    Resume,
    MainSiteContact,
    Blog
)


class CompanyTrackForm(forms.ModelForm):
    """
    This is a Django ModelForm for the CompanyTrack model.
    The CompanyTrackForm is used to display custom message to Hiring Managers when they open the website link in the
    Resume.

    Attributes:
        country (ChoiceField): A choice field that lists all countries. The choices are dynamically generated from the django_countries package.
        Meta: This inner class defines metadata for the form.
            model (CompanyTrack): The model that this form is associated with.
            fields (str): A special value '__all__' is used to indicate that all fields in the model should be used.
        Media: This inner class defines extra media to be used in the form.
            model (CompanyTrack): The model that this form is associated with.
            js (tuple): A tuple containing the paths to the JavaScript files to be included in the form.
    """

    # A choice field that lists all countries. The choices are dynamically generated from the django_countries package.
    country = forms.ChoiceField(
        choices=[(country.code, country.name) for country in countries],
    )

    class Meta:
        """
        This inner class defines metadata for the form.

        Attributes:
            model (CompanyTrack): The model that this form is associated with.
            fields (str): A special value '__all__' is used to indicate that all fields in the model should be used.
        """
        model = CompanyTrack
        fields = '__all__'
        # exclude = ['opened']

    class Media:
        """
        This inner class defines extra media to be used in the form.

        Attributes:
            model (CompanyTrack): The model that this form is associated with.
            js (tuple): A tuple containing the paths to the JavaScript files to be included in the form.
        """
        model = CompanyTrack
        js = ('main_site/script.js',)


class CompanyTrackAdmin(admin.ModelAdmin):
    """
    This is a Django ModelAdmin for the CompanyTrack model.

    Attributes:
        form (CompanyTrackForm): The form to be used in the admin interface for this model.
        list_display (tuple): A tuple containing the names of the fields of the model to be displayed in the list view of the admin interface.

    Methods:
        response_add(request, obj, post_url_continue=None): Overrides the response_add method of the ModelAdmin to redirect to a custom page after a new CompanyTrack object is added.
    """

    # The form to be used in the admin interface for this model.
    form = CompanyTrackForm

    # A tuple containing the names of the fields of the model to be displayed in the list view of the admin interface.
    list_display = (
        'tracker_id', 'company_name', 'applied_date', 'opened', 'country', 'city', 'position', 'url', 'opened_date',
        'note',
        'resume')

    def response_add(self, request, obj, post_url_continue=None):
        """
        Overrides the response_add method of the ModelAdmin to redirect to a custom page after a new CompanyTrack object is added.

        Parameters:
            request (HttpRequest): The request that led to the creation of the object.
            obj (CompanyTrack): The newly created object.
            post_url_continue (str, optional): The URL to redirect to. If None, a default URL is used.

        Returns:
            HttpResponseRedirect: A redirect response to the 'copy_page' view, with the primary key of the newly created object as an argument.
        """
        return HttpResponseRedirect(reverse('copy_page', args=(obj.pk,)))

    def delete_model(self, request, obj):
        """
        Overrides the delete_model method of the ModelAdmin to delete the resume file associated with the CompanyTrack object.
        """
        if obj.resume:
            obj.resume.delete()
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        """
        Overrides the delete_queryset method of the ModelAdmin to delete the resume files associated with the CompanyTrack objects.
        """
        for obj in queryset:
            if obj.resume:
                obj.resume.delete()
        super().delete_queryset(request, queryset)


class LicenseAdmin(admin.ModelAdmin):
    """
    This is a Django ModelAdmin for the License model.

    Attributes:
        list_display (list): A list containing the names of the fields of the model to be displayed in the list view of the admin interface.
        search_fields (list): A list containing the names of the fields of the model to be used in the search box in the admin interface.
    """

    # A list containing the names of the fields of the model to be displayed in the list view of the admin interface.
    list_display = ['license_key', 'name', 'active']

    # A list containing the names of the fields of the model to be used in the search box in the admin interface.
    search_fields = ['license_key']


class WebsiteAdmin(admin.ModelAdmin):
    """
    This is a Django ModelAdmin for the Website model.

    Attributes:
        list_display (list): A list containing the names of the fields of the model to be displayed in the list view of the admin interface.
        search_fields (list): A list containing the names of the fields of the model to be used in the search box in the admin interface.
        fields (tuple): A tuple containing the names of the fields to be displayed in the form in the admin interface.
    """

    list_display = ['name', 'url', 'license_key']

    search_fields = ['name']

    fields = ('name', 'url', 'license_key')


class ResumeAdmin(admin.ModelAdmin):
    """
    This is a Django ModelAdmin for the Resume model.
    Resume Model is used to store the updated resume of the user.
    """
    search_fields = ['name']

    def delete_model(self, request, obj):
        """
        Overrides the delete_model method of the ModelAdmin to delete the resume file associated with the Resume object.
        """
        if obj.file:
            obj.file.delete()
        super().delete_model(request, obj)

    def get_random_string(self, length):
        """
        Generate a random string of fixed length
        """
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def save_model(self, request, obj, form, change):
        """
        Overrides the save_model method of the ModelAdmin to append a random string to the filename of the resume file.

        """
        if obj.file:
            # append random string to the filename
            obj.file.name = obj.file.name.split('.')[0] + '_' + self.get_random_string(length=8) + '.' + \
                            obj.file.name.split('.')[1]
        super().save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        """
        Overrides the delete_queryset method of the ModelAdmin to delete the resume files associated with the Resume objects.
        """
        for obj in queryset:
            if obj.file:
                obj.file.delete()
        super().delete_queryset(request, queryset)


class BlogAdmin(admin.ModelAdmin):
    """
    This is a Django ModelAdmin for the Blog model.
    Blog Model is used to store the blog posts of the user.
    """

    form = BlogForm
    add_form = BlogAddForm

    def get_form(self, request, obj=None, **kwargs):
        """
        Overrides the get_form method of the ModelAdmin to use a different form for adding and changing objects.
        """
        if obj is None:
            return self.add_form
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        """
        Overrides the save_model method of the ModelAdmin to delete unused images when a blog post is approved.
        """
        if obj.approved:
            obj.delete_unused_images()
        super().save_model(request, obj, form, change)

    def render_change_form(self, request, context, *args, **kwargs):
        """
        Overrides the render_change_form method of the ModelAdmin to add the blog_id attribute to the content field.
        """
        if context['original'] is not None:
            context['adminform'].form.fields['content'].widget.attrs.update({
                'blog_id': context['original'].id
            })
        return super().render_change_form(request, context, args, kwargs)

    def delete_model(self, request, obj):
        """
        Overrides the delete_model method of the ModelAdmin to delete the images associated with the Blog object.
        """
        obj.delete_images(delete_folder=True)
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        """
        Overrides the delete_queryset method of the ModelAdmin to delete the images associated with the Blog objects.
        """
        for obj in queryset:
            obj.delete_images(delete_folder=True)
        super().delete_queryset(request, queryset)


# Register admin models

admin.site.register(License, LicenseAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(CompanyTrack, CompanyTrackAdmin)
admin.site.register(Api)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(MainSiteContact)
admin.site.register(Blog, BlogAdmin)
