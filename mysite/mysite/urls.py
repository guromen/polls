from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/polls/', permanent=False)),
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls'))
] + debug_toolbar_urls()
