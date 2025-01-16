from django.contrib import admin


from .models import UserProfile, UserPhoto,Persona

admin.site.register(UserProfile)
admin.site.register(UserPhoto)
admin.site.register(Persona)


# Register your models here
