from django.contrib import admin
from django.urls import path
from service import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # path('admin/', admin.site.urls),  # ✅ only once
    path('', views.combined_view, name='signup_login'),
    # path('login/', views.user_login, name='login'),
    path('home/', views.home, name='home'),
    path('items/', views.items),
    path('items/<int:itemId>/', views.itemDetails),
    path('dashboard/', views.dashboard, name='dashboard'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

