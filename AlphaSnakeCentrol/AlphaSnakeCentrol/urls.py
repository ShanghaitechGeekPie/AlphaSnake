"""AlphaSnakeCentrol URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin

from .views import homepage, postinit, postgo, getready, getmove, updategame


def blackhole(requests):
    import time
    time.sleep(10000)


urlpatterns = [
    url(r'^/?$', homepage),
    url(r'^init/?$', postinit),
    url(r'^go/?$', postgo),
    url(r'^ready/?$', getready),
    url(r'^move/?$', getmove),
    url(r'^update/?$', updategame),
    url(r'^blackhole/?$', blackhole),
    # url(r'^info/$', info),
    # url(r'^submit/$', submit),
    # url(r'^get_step/$', get_step),
    # url(r'^admin/', admin.site.urls),
]
