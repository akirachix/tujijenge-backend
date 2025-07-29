

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_remove_stock_image_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
