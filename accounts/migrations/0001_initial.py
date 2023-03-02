# Generated by Django 4.1.7 on 2023-03-02 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_alter_user_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ShopUser',
                'verbose_name_plural': 'ShopUsers',
            },
            bases=('core.user',),
        ),
    ]
