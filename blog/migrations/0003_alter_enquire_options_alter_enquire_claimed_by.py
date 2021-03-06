# Generated by Django 4.0.5 on 2022-06-30 06:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_enquire_claimed_by_alter_user_password'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='enquire',
            options={'ordering': ['pk']},
        ),
        migrations.AlterField(
            model_name='enquire',
            name='claimed_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='enquiry', to=settings.AUTH_USER_MODEL),
        ),
    ]
