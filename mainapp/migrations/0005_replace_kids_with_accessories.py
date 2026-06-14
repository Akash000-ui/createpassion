from django.db import migrations, models


def replace_kids_with_accessories(apps, schema_editor):
    Product = apps.get_model('mainapp', 'Product')
    Product.objects.filter(gender='Kids').update(gender='Accessories')


def replace_accessories_with_kids(apps, schema_editor):
    Product = apps.get_model('mainapp', 'Product')
    Product.objects.filter(gender='Accessories').update(gender='Kids')


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_add_income_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='gender',
            field=models.CharField(
                choices=[
                    ('Men', 'Men'),
                    ('Women', 'Women'),
                    ('Unisex', 'Unisex'),
                    ('Accessories', 'Accessories'),
                ],
                default='Unisex',
                max_length=20,
            ),
        ),
        migrations.RunPython(replace_kids_with_accessories, replace_accessories_with_kids),
    ]
