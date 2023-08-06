from django.conf.urls import url

from .views import  UploadSenderKey, Login, FetchOneTimeId, \
    UploadSenderKeys, UploadStandardSenderKeys, GetStickId

app_name = 'stick_protocol'
urlpatterns = [
    # url(r'^upload-pkb/$', UploadPreKeyBundle.as_view(), name='upload_pkb'),
    url(r'^upload-sk/$', UploadSenderKey.as_view(), name='upload_sk'),
    url(r'^upload-sks/$', UploadSenderKeys.as_view(), name='upload_sks'),
    url(r'^upload-standard-sks/$', UploadStandardSenderKeys.as_view(), name='upload_standard_sks'),
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^fetch-otid/$', FetchOneTimeId.as_view(), name='fetch_otid'),
    url(r'^get-stickId/$', GetStickId.as_view(), name='get_stickId'),
]