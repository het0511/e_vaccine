# Generated by Django 5.0.2 on 2024-03-23 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_vacc', '0003_alter_parent_user_contact_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor_user',
            name='contact_no',
            field=models.CharField(default='1234567890', max_length=10),
        ),
    ]
