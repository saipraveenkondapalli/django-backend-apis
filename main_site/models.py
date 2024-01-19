import datetime
import uuid

from django.db import models
from django_countries.fields import CountryField


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

