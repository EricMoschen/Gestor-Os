
from django.http import JsonResponse
from django.contrib import admin
from django.urls import path, include, redirect

def health_check(request):
    return JsonResponse({"status": "ok"})

def raiz(request):
    return redirect('menuos')  # nome da sua view menuos_view

urlpatterns = [
    path('', raiz),
    path('admin/', admin.site.urls),
    path('usuario/', include('usuario.urls')),
    path('menuos/', include('menuos.urls')),
    path('healthz/', health_check),
]
