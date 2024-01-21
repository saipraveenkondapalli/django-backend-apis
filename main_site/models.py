import datetime
import uuid
from typing import List

from bs4 import BeautifulSoup
from django.db import models
from django_countries.fields import CountryField

import cloudinary.api


class Website(models.Model):
    license_key = models.ForeignKey('License', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    url = models.URLField()
    last_visit = models.DateTimeField(auto_now=True)
    total_visits = models.IntegerField(default=0)
    locations = models.ManyToManyField('Location', blank=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100)
    total_visits = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.city}, {self.country}"


class CompanyTrack(models.Model):
    tracker_id = models.UUIDField(primary_key=True, auto_created=True, editable=False, default=uuid.uuid4)

    company_name = models.CharField(max_length=100)
    applied_date = models.DateTimeField(default=datetime.datetime.now)
    opened = models.BooleanField(default=False)
    country = CountryField()
    city = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    url = models.TextField()
    opened_date = models.DateTimeField(auto_now=True)
    note = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def delete(self, *args, **kwargs):
        if self.resume:
            self.resume.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.company_name} - {self.position}"


class License(models.Model):
    license_key = models.UUIDField(primary_key=True, auto_created=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    apis = models.ManyToManyField('Api', blank=True)

    def __str__(self):
        return self.name


class Api(models.Model):
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Resume(models.Model):
    file = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.file.name


class MainSiteContact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name


class Blog(models.Model):
    content = models.TextField()
    created_date = models.DateTimeField(default=datetime.datetime.now)
    title = models.CharField(max_length=130)
    slug = models.SlugField(max_length=150, unique=True)  # slug eg:- this-is-a-blog-post
    active = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def delete(self, using=None, keep_parents=False):
        self.delete_images(delete_folder=True)
        super().delete(using, keep_parents)

    def delete_images(self, public_ids=None, delete_folder: bool = False):

        if public_ids is None:
            public_ids = BlogImage.objects.filter(blog=self).values_list('public_id', flat=True)
            public_ids = list(public_ids)
        if public_ids:
            cloudinary.api.delete_resources(public_ids, resource_type='image', type='upload')

        if public_ids and delete_folder:
            cloudinary.api.delete_folder(f'blog/{self.id}')
            BlogImage.objects.filter(public_id__in=public_ids).delete()

    def _get_image_tags(self):
        soup = BeautifulSoup(self.content, 'html.parser')
        img_tags = soup.find_all('img')
        return img_tags

    def _get_image_urls(self):
        img_tags = self._get_image_tags()
        urls = [img['src'] for img in img_tags if 'src' in img.attrs]
        return urls

    def _get_public_ids(self):
        urls = self._get_image_urls()
        # public ids look like "blog/{blog_id}/{image_name}" we need include blog/{blog_id}/image name

        public_ids = BlogImage.objects.filter(url__in=urls).values_list('public_id', flat=True)

        return public_ids

    def _unused_images(self):
        present = self._get_public_ids()
        # find unused images by comparing original and public_ids from BlogImage
        all_blog_images = BlogImage.objects.filter(blog=self)
        diff = set(all_blog_images) - set(present)
        return list(diff)

    def delete_unused_images(self):
        unused_images = self._unused_images()
        public_ids = [image.public_id for image in unused_images]
        self.delete_images(public_ids)


class BlogImage(models.Model):
    public_id = models.CharField(max_length=150)
    url = models.URLField(default='')
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
