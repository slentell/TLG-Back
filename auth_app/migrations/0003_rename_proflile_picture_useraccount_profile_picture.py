

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0002_alter_useraccount_proflile_picture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraccount',
            old_name='proflile_picture',
            new_name='profile_picture',
        ),
    ]
