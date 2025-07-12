from django.contrib import admin
from django.urls import path
from service import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # path('admin/', admin.site.urls),  # ✅ only once
    path('', views.combined_view, name='signup_login'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('add_user/', views.add_user_info, name='addUser'),
    path('addItems/', views.addItems, name = 'addItems'),
    path('items/<int:itemId>/', views.itemDetails),
    path('dashboard/', views.dashboard, name='dashboard'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

