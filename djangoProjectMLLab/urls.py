from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import djangoProjectMLLab
from djangoProjectMLLab.views import upload_file, show_results, delete_prediction

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', upload_file),
    path('show_results/', show_results, name='show_results'),
    path('delete_prediction/<int:prediction_id>/', delete_prediction, name='delete_prediction'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
