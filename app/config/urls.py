from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),    # tutte le view di inventory
]
    # EntrataMerci/app/config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views # <<<< IMPORTA QUESTO
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # URLs per l'autenticazione
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'), # <<<< AGGIUNGI QUESTA
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'), # <<<< AGGIUNGI QUESTA

    # Include le URL della tua app 'inventory'
    path('inventory/', include('inventory.urls')), # Aggiunto prefisso 'inventory/' per chiarezza
                                                # Se preferisci alla root, lascia '' come prima

    # Eventuale URL radice se non gestita da inventory.urls
    # path('', una_tua_vista_home_generale, name='home_sito'), # Se inventory non è alla root
]

# Per servire media files e static files durante lo sviluppo (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # La riga sotto per static files è spesso gestita da Django stesso in dev,
    # ma non fa male esplicitarla se usi `collectstatic` anche in dev.
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)