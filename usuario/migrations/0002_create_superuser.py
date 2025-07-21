from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    if not User.objects.filter(username='admin').exists():
        User.objects.create(
            username='admin',
            email='admin@email.com',
            is_staff=True,
            is_superuser=True,
            is_active=True,
            password=make_password('admin123')  # Defina sua senha aqui
        )

class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),  # ajuste se seu último número for diferente
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
