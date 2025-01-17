# Generated by Django 5.1.5 on 2025-01-20 06:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Auth', '0001_initial'),
        ('Books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Borrowing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_at', models.DateTimeField(auto_now_add=True)),
                ('stripe_payment_intent_id', models.CharField(blank=True, max_length=255, null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Books.book')),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auth.auth')),
            ],
        ),
    ]
