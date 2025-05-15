# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('inventory.urls')),    # tutte le view di inventory
# ]
# ingresso/EntrataMerci/app/config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views # <<<< IMPORTA QUESTO
from django.conf import settings # Per servire media files in dev
from django.conf.urls.static import static # Per servire media files in dev

urlpatterns = [
    path('admin/', admin.site.urls),
    # URLs per l'autenticazione
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'), # <<<< AGGIUNGI QUESTA
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'), # <<<< AGGIUNGI QUESTA

    # Include le URL della tua app 'inventory'
    # Assicurati che l'app 'inventory' abbia un app_name = 'inventory' nel suo urls.py se usi il namespace
    path('', include('inventory.urls')), # O il prefisso che usi, es. 'inventory/'
]

# Per servire media files durante lo sviluppo (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Anche se WhiteNoise potrebbe gestirli