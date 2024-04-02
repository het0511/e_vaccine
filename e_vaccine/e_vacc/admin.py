from django.contrib import admin
from .models import *;
# Register your models here.

class parent_admin(admin.ModelAdmin):
    list_display = ['fullname','username','email','contact_no','password']
admin.site.register(parent_user,parent_admin)

class hospital_admin(admin.ModelAdmin):
    list_display = ['hospital_name','address','license_no']
admin.site.register(hospital_user,hospital_admin)

class doctor_admin(admin.ModelAdmin):
    actions = ["change_status","c_status","ch_status"]
    @admin.action(description="Change status to active")
    def change_status(self, request, queryset):
        queryset.update(status="active")
    @admin.action(description="Change status to pending")
    def c_status(self, request, queryset):
        queryset.update(status="pending")
    @admin.action(description="Change status to rejected")
    def ch_status(self, request, queryset):
        queryset.update(status="rejected")
    list_display = ['doctor_name','hospital_id','email','contact_no','username','password','status']
admin.site.register(doctor_user,doctor_admin)

class child_admin(admin.ModelAdmin):
    list_display = ['name','date_of_birth','age','address','parent_id']
admin.site.register(child_data,child_admin)

class vaccine_admin(admin.ModelAdmin):
    list_display = ['vaccine_name']
admin.site.register(vaccine,vaccine_admin)

class appointment_admin(admin.ModelAdmin):
    list_display = ['hospital_name','child_name','date','time','vaccine_id','status','parent_id']
admin.site.register(appointment,appointment_admin)