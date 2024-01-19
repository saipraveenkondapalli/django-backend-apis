import json

from django.http import JsonResponse, FileResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from main_site.decorator import check_license
from main_site.models import Website, CompanyTrack, Resume
from main_site.utils import get_ip_address_data
from .models import MainSiteContact
from .utils import EmailHandler


def copy_page(request, pk):
    return render(request, 'admin/copy_id.html', {'pk': pk})


@check_license('web')
def web(request):
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
    id = request.GET.get('id')
    company = CompanyTrack.objects.get(tracker_id=id)
    company.opened = True
    company.save()
    EmailHandler().send_company_track_alert(company)
    return HttpResponse('success')


def resume(request):
    tracker_id = request.GET.get('id')
    if tracker_id:
        company = CompanyTrack.objects.get(tracker_id=tracker_id)
        file = company.resume.storage.open(company.resume.name, 'rb')
        return FileResponse(file)


def main_resume(request):
    file = Resume.objects.first()
    if not file:
        return HttpResponse('No resume found')
    file = file.file.storage.open(file.file.name, 'rb')

    return FileResponse(file, as_attachment=False, filename="sai_praveen_kondapalli_resume." + file.name.split('.')[-1])


@csrf_exempt
def contact_send_email(request):
    data = json.loads(request.body)

    try:
        new_contact = MainSiteContact.objects.create(
            name=data.get('name'),
            email=data.get('email'),
            message=data.get('message'),
        )
        EmailHandler().send_contact_email(new_contact)
    except Exception as _:
        return HttpResponse('error')
    return HttpResponse('success')
