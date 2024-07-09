from django.urls import include, path
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

API_TITLE = 'Lingo Club API'
API_DESCRIPTION = 'A Web API for creating and managing lingo club meetings.'
schema_view = get_schema_view(title=API_TITLE)

urlpatterns = [
    path('clubusers/', include('clubusers.urls')),
    path('meetings/', include('meetings.urls')),
]


# To enable login in the webUI, these part is a-must.
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += [
    path('schema/', schema_view),
    path('docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION))
]
