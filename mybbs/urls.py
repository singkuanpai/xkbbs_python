from django.conf.urls.defaults import * 
import mybbs

urlpatterns = patterns('', 
    url(r'^about/$',mybbs.views.about),
    url(r'^w/$',mybbs.views.post_write),
    url(r'^list/$',mybbs.views.post_list),
    url(r'^view/$',mybbs.views.post_view),



)

