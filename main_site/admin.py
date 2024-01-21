import random
import string

from django import forms
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django_countries import countries
from django.contrib.auth.hashers import check_password

from .forms import BlogForm, BlogAddForm, AuthenticateWithPasswordForm
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
    country = forms.ChoiceField(
        choices=[(country.code, country.name) for country in countries],
    )

    class Meta:
        model = CompanyTrack
        fields = '__all__'
        exclude = ['opened']

    class Media:
        model = CompanyTrack
        js = ('main_site/script.js',)


class CompanyTrackAdmin(admin.ModelAdmin):
    form = CompanyTrackForm
    list_display = (
        'tracker_id', 'company_name', 'applied_date', 'opened', 'country', 'city', 'position', 'url', 'opened_date',
        'note',
        'resume')

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect(reverse('copy_page', args=(obj.pk,)))

    def delete_model(self, request, obj):
        if obj.resume:
            obj.resume.delete()
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.resume:
                obj.resume.delete()
        super().delete_queryset(request, queryset)


class LicenseAdmin(admin.ModelAdmin):
    list_display = ['license_key', 'name', 'active']
    search_fields = ['license_key']


class WebsiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'license_key']
    search_fields = ['name']
    fields = ('name', 'url', 'license_key')


class ResumeAdmin(admin.ModelAdmin):
    search_fields = ['name']

    def delete_model(self, request, obj):
        if obj.file:
            obj.file.delete()
        super().delete_model(request, obj)

    def get_random_string(self, length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def save_model(self, request, obj, form, change):
        if obj.file:
            # append random string to the filename
            obj.file.name = obj.file.name.split('.')[0] + '_' + self.get_random_string(length=8) + '.' + \
                            obj.file.name.split('.')[1]
        super().save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.file:
                obj.file.delete()
        super().delete_queryset(request, queryset)


class BlogAdmin(admin.ModelAdmin):
    form = BlogForm
    add_form = BlogAddForm

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return self.add_form
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if obj.approved:
            obj.delete_unused_images()
        super().save_model(request, obj, form, change)

    def render_change_form(self, request, context, *args, **kwargs):
        if context['original'] is not None:
            context['adminform'].form.fields['content'].widget.attrs.update({
                'blog_id': context['original'].id
            })
        return super().render_change_form(request, context, args, kwargs)

    def delete_model(self, request, obj):
        obj.delete_images(delete_folder=True)
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete_images(delete_folder=True)
        super().delete_queryset(request, queryset)


admin.site.register(License, LicenseAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(CompanyTrack, CompanyTrackAdmin)
admin.site.register(Api)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(MainSiteContact)
admin.site.register(Blog, BlogAdmin)
