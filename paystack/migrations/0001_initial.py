# Generated by Django 2.2.3 on 2019-08-14 23:08

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=60)),
                ('reference', models.CharField(max_length=50)),
                ('data', jsonfield.fields.JSONField(default=dict)),
            ],
        ),
    ]