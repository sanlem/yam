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
from users import views as users_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/messages/', include(messages_router.urls)),
    url(r'^api/chats/(?P<pk>[0-9]+)/$', chat_views.ChatDetailView.as_view(),
        name="chat-detail"),
    url(r'^api/chats/$', chat_views.ChatsView.as_view(), name="chat-list"),
    url(r'^api/chats/leave/$', chat_views.LeaveChatView.as_view(), name="chat-leave"),
    url(r'^api/chats/add_user/$', chat_views.AddToChatView.as_view(), name="chat-add"),

    url(r'^api/users/$', users_views.RegistrationView.as_view(), name="users-list"),
    url(r'^api/users/me/$', users_views.CurrentUserInfoView.as_view(), name="users-me"),
    url(r'^api/users/blocked/add/$', users_views.BlockUserView.as_view(),
        name="users-block"),
    url(r'^api/users/blocked/remove/$', users_views.UnlockUserView.as_view(),
        name="users-unlock"),
    url(r'^api/users/contacts/add/$', users_views.AddToContactsView.as_view(),
        name="users-add-to-contacts"),
    url(r'^api/users/contacts/remove/$', users_views.RemoveFromContactsView.as_view(),
        name="users-remove-from-contacts"),
]
