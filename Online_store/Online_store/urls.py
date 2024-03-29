from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls',namespace='shop')),
]


# обслуживания медиа-файлов во время разработки
#!!!! пока не очень вникаю зачем это вообще
if settings.DEBUG:
    # проверяет, включен ли режим отладки в настройках проекта (settings.DEBUG).
    # Режим отладки обычно включен во время разработки и должен быть выключен в продакшн.

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    # В этих строках к списку URL-паттернов urlpatterns добавляются пути, которые позволяют
    # обслуживать медиа-файлы во время разработки. Функция static() используется для добавления
    # URL-паттернов, которые обращаются к медиа-файлам по URL, определенному в
    # settings.MEDIA_URL, и отдают их из директории, указанной в settings.MEDIA_ROOT.

