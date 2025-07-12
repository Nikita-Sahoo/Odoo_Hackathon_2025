from django.contrib import admin
from .models import Login, Item, UserDetails # import your actual model

admin.site.register(Login)
admin.site.register(Item)
admin.site.register(UserDetails)
# admin.site.register(Login)