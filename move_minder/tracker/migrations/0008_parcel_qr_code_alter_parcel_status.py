# Generated by Django 5.0.2 on 2024-04-04 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0007_alter_move_secondary_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcel',
            name='qr_code',
            field=models.ImageField(blank=True, max_length=255, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='status',
            field=models.CharField(choices=[('Packed', 'Packed'), ('In Transit', 'In Transit'), ('Lost', 'Lost'), ('Received', 'Received'), ('Damaged', 'Damaged'), ('Accepted', 'Accepted')], default='Packed', max_length=12),
        ),
    ]