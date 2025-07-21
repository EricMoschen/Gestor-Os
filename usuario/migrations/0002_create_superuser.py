from django.db import migrations
from django.contrib.auth.hashers import make_password

def criar_superusuario(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    
    if not User.objects.filter(username='admin').exists():
        User.objects.create(
            username='admin',
            email='admin@example.com',
            is_staff=True,
            is_superuser=True,
            is_active=True,
            password=make_password('senha123')  # Troque por uma senha forte
        )

class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ]

    operations = [
        migrations.RunPython(criar_superusuario),
    ]
