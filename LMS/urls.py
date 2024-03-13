from django.contrib import admin
from django.urls import path,include
from .import views, user_login
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from payment.views import callback_gateway_view
from azbankgateways.urls import az_bank_gateways_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('base', views.BASE,name='base'),
    path('404', views.PAGE_NOT_FOUND,name='404'),
    path('', views.HOME,name='home'),
    path('courses', views.SINGLE_COURSE,name='single_course'),
    path('courses/filter-data',views.filter_data,name="filter-data"),
    path('course/<slug:slug>',views.COURSE_DETAILS,name="course_details"),
    path('search',views.SEARCH_COURSE,name='search_course'),
    path('contact', views.CONTACT_US,name='contact_us'),
    path('about', views.ABOUT_US,name='about_us'),
    path('accounts/register', user_login.REGISTER,name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('doLogin', user_login.DOLOGIN,name='dologin'),
    path('logout',user_login.LOGOUT,name='logout'),
    path('accounts/profile', user_login.PROFILE,name='profile'),
    path('accounts/profile/update', user_login.PROFILE_UPDATE,name='profile_update'),
    path('my-course',views.MY_COURSE,name="my_course"),
    path('course/watch-course/<slug:slug>',views.WATCH_COURSE,name="watch_course"),
    path('cart/', include('cart.urls')),
    path('order/', include('orders.urls')),
    path('payment/', include('payment.urls')),
    path('coupons/', include('coupons.urls')),
    path('bankgateways/', az_bank_gateways_urls()),
    path('callback-gateway', callback_gateway_view),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
