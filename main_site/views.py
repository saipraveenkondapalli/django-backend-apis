import json

import cloudinary.uploader
import django.utils.log
from django.core import serializers
from django.http import FileResponse, JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from main_site.decorator import check_license
from main_site.models import Website, CompanyTrack, Resume, BlogImage, Blog
from main_site.utils import get_ip_address_data
from .models import MainSiteContact
from .utils import EmailHandler


def copy_page(request, pk):
    """
    Render a page with a copy of the ID.

    :param request: The HTTP request.
    :param pk: The primary key of the object to copy.
    :return: Rendered HTML page.
    """
    return render(request, 'admin/copy_id.html', {'pk': pk})


@check_license('web')
def web(request):
    """
    Handle a web request and increment the total visits of the website and location.

    :param request: The HTTP request.
    :return: JsonResponse with a success message.
    """
    website = Website.objects.get(license_key=request.GET.get('id'))
    website.total_visits += 1

    location_data = get_ip_address_data(request.META.get('REMOTE_ADDR'))
    location, created = website.locations.get_or_create(
        country=location_data.get('country'),
        city=location_data.get('city'),
        zip=location_data.get('zip'),
        ip_address=location_data.get('query'),
    )
    location.total_visits += 1
    location.save()
    website.save()
    return JsonResponse({'msg': 'success'})


def job_application(request):
    """
    Handle a job application request and send an email alert.

    :param request: The HTTP request.
    :return: HttpResponse with the serialized company object.
    """
    id = request.GET.get('id')
    company = CompanyTrack.objects.get(tracker_id=id)
    company.opened = True
    company.save()
    EmailHandler().send_company_track_alert(company)
    #     return entire model as json
    company_json = serializers.serialize('json', [company, ])

    return HttpResponse(company_json, content_type='application/json')


def resume(request):
    """
    Handle a resume request.

    :param request: The HTTP request.
    :return: FileResponse with the resume file.
    """
    tracker_id = request.GET.get('id')
    if tracker_id:
        company = CompanyTrack.objects.get(tracker_id=tracker_id)
        file = company.resume.storage.open(company.resume.name, 'rb')
        return FileResponse(file)


def main_resume(request):
    """
    Handle a main resume request.

    :param request: The HTTP request.
    :return: FileResponse with the main resume file.
    """
    file = Resume.objects.first()
    if not file:
        return HttpResponse('No resume found')
    file = file.file.storage.open(file.file.name, 'rb')

    return FileResponse(file, as_attachment=False, filename="sai_praveen_kondapalli_resume." + file.name.split('.')[-1])


@csrf_exempt
def contact_send_email(request):
    """
    Handle a contact send email request.

    :param request: The HTTP request.
    :return: HttpResponse with a success or error message.
    """
    data = json.loads(request.body)

    try:
        new_contact = MainSiteContact.objects.create(
            name=data.get('name'),
            email=data.get('email'),
            message=data.get('message'),
        )
        try:
            EmailHandler().send_contact_email(new_contact)
        except Exception as _:
            django.utils.log.log_response("Error sending email"
                                          " to contact: " + str(new_contact.email))

    except Exception as _:
        return HttpResponse('error')
    return HttpResponse('success')


@csrf_exempt
def upload_image(request):
    """
    Handle an upload image request.

    :param request: The HTTP request.
    :return: JsonResponse with the image URL or an error message.
    """
    if request.method == 'POST':
        blog_id = request.GET.get('blog_id')
        blog = Blog.objects.get(id=blog_id) if blog_id else None
        if not blog:
            return JsonResponse({'error': 'Invalid blog id'})

        file = request.FILES['upload']
        folder = f'blog/{blog_id}'
        upload_result = cloudinary.uploader.upload(file, folder=folder)
        BlogImage.objects.create(
            blog=blog,
            public_id=upload_result['public_id'],
            url=upload_result['url']
        )

        return JsonResponse({
            'url': upload_result['url'],
        })

    return JsonResponse({'error': 'Invalid method'})
