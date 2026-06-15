from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_replace_kids_with_accessories'),
    ]

    operations = [
        migrations.AddField(
            model_name='companydocument',
            name='google_drive_url',
            field=models.URLField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='companydocument',
            name='document_file',
        ),
    ]
