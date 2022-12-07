from django.urls import path
from .views import *

urlpatterns = [
    path('mailing', MailApiStart.as_view()),
    path('stat/mailings', MailingApiView.as_view()),
    path('stat/mailings/<int:pk>', MailingApiUpdate.as_view()),
    path('clients', ClientApiList.as_view()),
    path('clients/<int:pk>', ClientApiUpdate.as_view()),
    path('stat/messages/<int:pk>', StatApiMessages.as_view()),
    path('stat/messages', StatVApiMessages.as_view()),
    path('stat', StatApiGlobal.as_view())
]