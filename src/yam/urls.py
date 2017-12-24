"""yam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from chat_messages.urls import router as messages_router
from chat_messages import views as chat_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^messages/', include(messages_router.urls)),
    url(r'^chats/(?P<pk>[0-9]+)/$', chat_views.ChatDetailView.as_view(), name="chat-detail"),
    url(r'^chats/$', chat_views.ChatsView.as_view(), name="chat-list"),
]
