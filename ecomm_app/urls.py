from django.urls import path
from ecomm_app import views
from ecomm import settings
from django.conf.urls.static import static

urlpatterns = [
    path('index/', views.index),
    path('contact', views.contact),
    path('placement', views.placement),
    path('edit/<rid>', views.edit),
    path('delete/<rid>', views.delete),
    path('myview',views.SimpleView.as_view()),
    path('hello', views.hello),
    path('pdetails/<pid>', views.pdetails),
    path('register', views.register),
    path('login', views.user_login),
    path('logout', views.user_logout),
    path('catfilter/<cv>', views.catfilter),
    path('sort/<sv>', views.sort),
    path('range', views.range),
    path('addtocart/<pid>', views.addtocart),
    path('viewcart', views.viewcart),
    path('remove/<cid>', views.remove),
    path('updateqty/<qv>/<cid>', views.updateqty),
    path('placeorder', views.placeorder),
    path('makepayment', views.makepayment),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)