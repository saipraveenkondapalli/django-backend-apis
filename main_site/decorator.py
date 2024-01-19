from functools import wraps
from django.http import HttpResponseForbidden
from .models import License, Website


def check_license(api_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            license_key = request.GET.get('id')
            try:
                license = License.objects.get(license_key=license_key)
            except License.DoesNotExist:
                return HttpResponseForbidden()

            if license.active and license.apis.filter(name=api_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                print('License is not active')
                return HttpResponseForbidden()

        return _wrapped_view

    return decorator

