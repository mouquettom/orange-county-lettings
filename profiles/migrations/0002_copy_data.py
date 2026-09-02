from django.db import migrations


def copy_profiles_data(apps, schema_editor):

    OldProfile = apps.get_model('oc_lettings_site', 'Profile')
    NewProfile = apps.get_model('profiles', 'Profile')

    for old_profile in OldProfile.objects.all():
        NewProfile.objects.create(
            id=old_profile.id,
            user_id=old_profile.user_id,
            favorite_city=old_profile.favorite_city,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('oc_lettings_site', '0002_auto_20260819_0849'),
    ]

    operations = [
        migrations.RunPython(copy_profiles_data),
    ]