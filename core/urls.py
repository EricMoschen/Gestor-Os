
from django.http import JsonResponse
from django.contrib import admin
from django.urls import path, include

def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuario/', include('usuario.urls')),
    path('menuos/', include('menuos.urls')),
    path('healthz/', health_check),
]
