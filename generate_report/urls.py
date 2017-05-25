"""generate_report URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from category.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', get_list_of_categories),
    url(r'^subcategories/$', get_list_of_sub_categories, name='sub-categories'),
    url(r'^reports/$', get_reports_for_sub_categories, name='reports'),
    url(r'^report/(?P<report_id>[0-9]+)/reports/$', get_report_detail, name='report-detail'),
    # url(r'^$', include('category.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
