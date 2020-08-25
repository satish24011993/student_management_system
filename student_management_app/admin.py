from django.contrib import admin

# Register your models here.

# we are creating blank usermodel class and registering into admin.py if i don't create blank usermodel then password will not be encrypted you can try it removing this blank usermodel 
from django.contrib.auth.admin import UserAdmin

from student_management_app.models import CustomUser

class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser, UserModel)
