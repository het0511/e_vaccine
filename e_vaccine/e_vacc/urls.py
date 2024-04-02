from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('hospital_login/',views.hospital_login,name='hospital_login'),
    path('parent_login/',views.parent_login,name='parent_login'),
    path('new_doctor/',views.new_doctor,name='new_doctor'),
    path('new_parent/',views.new_parent,name='new_parent'),
    path('hospital_dashboard/',views.hospital_dashboard,name='hospital_dashboard'),
    path('hospital_logout/',views.hospital_logout,name='hospital_logout'),
    path('parent_logout/',views.parent_logout,name='parent_logout'),
    path('appointment/',views.appointment1,name='appointment'),
    path('manage_child_data/',views.manage_child_data,name='manage_child_data'),
    path('book_appointment/',views.book_appointment,name='book_appointment'),
    path('view_child_data/<int:appointment_id>/', views.view_child_data, name='view_child_data'),
    path('edit_appointment/<int:appointment_id>/', views.doctor_edit_appointment, name='edit_appointment'),
    path('delete_appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('parent_edit_appointment/<int:appointment_id>/', views.edit_appointment, name='parent_edit_appointment'),
]