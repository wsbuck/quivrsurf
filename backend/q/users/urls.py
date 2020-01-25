from django.urls import path
from django.conf.urls import url

from users import views

urlpatterns = [
    # path('', views.UserList.as_view(), name='user-list'),
    path('create/', views.UserCreate.as_view(), name='user-create'),
    url(r'^activate/(?P<pk>\d+)/(?P<token>[\w.:\-_=]+)/$',
            views.activate, name="activate"),
]
