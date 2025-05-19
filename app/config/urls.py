    # EntrataMerci/app/config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect # <<<< Importa redirect
from inventory import views as inventory_views # <<<< Importa le viste di inventory

# Una vista semplice per reindirizzare o mostrare qualcosa
def root_redirect_view(request):
    if request.user.is_authenticated:
        return redirect('inventory:home_inventory') # Nome della tua URL per la dashboard inventario
    return redirect('login') # Nome della tua URL per il login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('inventory/', include('inventory.urls')), # Le URL della tua app inventario

    # path('', inventory_views.home_inventory, name='home_root'), # Opzione se vuoi usare la dashboard come root
    path('', root_redirect_view, name='home_root'), # <<<< AGGIUNGI QUESTA PER LA ROOT

    # Media files (mantenuto per completezza, ma la gestione statica/media in prod è diversa)
    # path('^media/(?P<path>.*)$', ... ) # Questa sintassi è per re_path, non path
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Questa è opzionale in dev con runserver