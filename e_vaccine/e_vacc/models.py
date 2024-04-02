from django.db import models

# Create your models here.
class parent_user(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    contact_no = models.CharField(max_length=10, default='1234567890')
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=20)
    def __str__(self):
        return self.username

class hospital_user(models.Model):
    hospital_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    license_no = models.IntegerField()
    def __str__(self):
        return self.hospital_name

class doctor_user(models.Model):
    doctor_name = models.CharField(max_length=255)
    hospital_id = models.ForeignKey(hospital_user, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, default='abcd@gmail.com')
    contact_no = models.CharField(max_length=10, default='1234567890')
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    def __str__(self):
        return self.username

class child_data(models.Model):
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    address = models.CharField(max_length=255)
    parent_id = models.ForeignKey(parent_user, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class vaccine(models.Model):
    vaccine_name = models.CharField(max_length=255)
    def __str__(self):
        return self.vaccine_name

class appointment(models.Model):
    hospital_name = models.CharField(max_length=255)
    child_name = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    vaccine_id = models.ForeignKey(vaccine, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    parent_id = models.ForeignKey(parent_user, on_delete=models.CASCADE)
    def __str__(self):
        return self.child_name

class administered(models.Model):
    administered_id = models.AutoField(primary_key=True)
    doctor_id = models.ForeignKey(doctor_user, on_delete=models.CASCADE)
    appointment_id = models.ForeignKey(appointment, on_delete=models.CASCADE)
    def __str__(self):
        return self.administered_id