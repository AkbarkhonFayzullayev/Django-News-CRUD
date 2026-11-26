from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

urlpatterns = [
    path('',index, name='home'),
    path('categories/<int:category_id>',categories,name='categories'),
    path('new_about/<int:new_id>',new_about,name='new_about'),
    path('add_news/',add_news,name='add_news'),
    path('update_new/<int:new_id>',update_new,name='update_new'),
    path('add_category/',add_categories,name='add_categories'),
    # path('', index, name='home'),
    path('login',LoginPage, name='Login'),
    path("search-news/", search_news, name="search-news"),
    path("delete/<news_id>", delete_news, name="delete_news"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
