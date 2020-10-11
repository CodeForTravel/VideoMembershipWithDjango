# Generated by Django 3.1.2 on 2020-10-08 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0002_membership_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='membership_type',
            field=models.CharField(choices=[('Enterprise', 'Enterprise'), ('Professional', 'Professional'), ('Free', 'Free')], default='Free', max_length=100),
        ),
    ]
