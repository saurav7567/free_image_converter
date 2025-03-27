from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.base, name='base'),  
    path('about/', views.about, name='about'),
    path('mergepdf/', views.mergepdf, name='mergepdf'),
    path('home/', views.home, name='home'),
    path('png/', views.png, name='png'),
    path('jpgs/', views.jpgs, name='jpgs'),
    path('jpeg/', views.jpeg , name = 'jpeg'),
    path('webp/' , views.webp , name = 'webp'),
    path('imagestopdf/' , views.image_to_pdf , name = 'image_to_pdf'),
    path('uploadimg/' , views.uploadimg , name = 'uploadimg'),
    path('resize/', views.resize , name = 'resize'),
    path('crop/', views.crop , name = 'crop'),
    path('grascale/', views.grascale , name = 'grascale'),
    path('Remove/' , views.Remove , name = 'Remove'),
    path('pdf_compressor/' , views.pdf_compressor , name = 'pdf_compressor'),
    path('pdf_to_word/' , views.pdf_to_word , name = 'pdf_to_word'),
    path('word_to_pdf/' , views.word_to_pdf , name = 'word_to_pdf'),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
