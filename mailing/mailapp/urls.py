from django.urls import path
from .yasg import urlpatterns as url_yasg
from .views import *

urlpatterns = [
    path('mailing', MailApiCreate.as_view()),
    path('mailing/<int:pk>', MailingApiUpdate.as_view()),
    path('client', ClientApiCreate.as_view()),
    path('client/<int:pk>', ClientApiUpdate.as_view()),
    path('stat', StatApiGlobal.as_view()),
    path('stat/mailings', StatApiMailings.as_view()),
    path('stat/clients', StatApiClients.as_view()),
    path('stat/messages', StatApiMessages.as_view()),
    path('stat/messages/<int:pk>', StatVApiMessages.as_view()),
]

urlpatterns += url_yasg
