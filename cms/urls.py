from django.conf.urls import url
#from django.contrib import admin
#from django.conf.urls import include
from cms import views
#from cms.views import Collection
#from django.conf import settings
#from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^collection/$', views.collection, name='collection'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    #url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^artist/(?P<artist_name_slug>[\w\-]+)/$', views.show_artist, name='show_artist'),
    url(r'^item/(?P<item_id>[\w\-]+)/$', views.show_item, name='show_item'),
    url(r'^edit_item/$', views.edit_item_search, name='restricted'),
    url(r'^edit_item/(?P<item_id>[\w\-]+)/$', views.edit_item, name='edit_item'),
    url(r'^edit_artist/$', views.edit_artist_search, name='edit_artist_search'),
    url(r'^edit_artist/(?P<artist_name_slug>[\w\-]+)/$', views.edit_artist, name='edit_artist'),
    url(r'^edit_category/$', views.edit_category_search, name='edit_category_search'),
    url(r'^edit_category/(?P<category_name_slug>[\w\-]+)/$', views.edit_category, name='edit_category'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^add_artist/$', views.add_artist, name='add_artist'),
    url(r'^add_item/$', views.add_item, name='add_item'),
    url(r'^delete_category/$', views.delete_category, name='delete_category'),
    url(r'^delete_artist/$', views.delete_artist, name='delete_artist'),
    url(r'^delete_item/$', views.delete_item, name='delete_item'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
]



