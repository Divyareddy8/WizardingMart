# Generated by Django 5.0.3 on 2024-04-02 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_order_customer_delete_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.DeleteModel(
            name='Size',
        ),
    ]
