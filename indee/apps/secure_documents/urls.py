from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^document/$', UserDocuments.as_view(), name='user_document'),
    url(r'^secureview/(?P<sec_doc_id>\w+)/$', SharedSecureDocument.as_view(), name='shared_doc_view'),
    url(r'^login/$', UserLogin.as_view(), name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/app1/login/'}),
]
