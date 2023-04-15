# Generated by Django 4.1.7 on 2023-04-07 08:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('Case_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Case_Name', models.CharField(max_length=50, verbose_name='Название кейса')),
                ('Case_Comment', models.TextField(verbose_name='Коментарий')),
                ('Case_Parent', models.IntegerField(default=-1, verbose_name='Родительский кейс')),
            ],
            options={
                'verbose_name': 'Кейс',
                'verbose_name_plural': 'Кейсы',
            },
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('Parameter_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Parameter_Name', models.CharField(max_length=100, verbose_name='Название')),
                ('Parameter_Comment', models.TextField(verbose_name='Коментарий')),
                ('Parameter_Sort', models.FloatField(default=models.AutoField(primary_key=True, serialize=False), null=True, verbose_name='Вес при сортировке')),
            ],
            options={
                'verbose_name': 'Параметр',
                'verbose_name_plural': 'Параметры',
            },
        ),
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('Variable_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Variable_Name', models.CharField(max_length=100, verbose_name='Переменная')),
                ('parameter', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cases.parameter')),
            ],
            options={
                'verbose_name': 'Переменная',
                'verbose_name_plural': 'Переменные',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('Status_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Status_Name', models.CharField(max_length=50, verbose_name='Статус работы')),
                ('Status_Comment', models.TextField(verbose_name='Коментарий')),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
            options={
                'verbose_name': 'Статус работы',
                'verbose_name_plural': 'Статусы работы',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('Section_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Section_Name', models.CharField(max_length=100, verbose_name='Название раздела')),
                ('Section_Sort', models.FloatField(default=models.AutoField(primary_key=True, serialize=False), null=True, verbose_name='Вес при сортировке')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.case')),
            ],
            options={
                'verbose_name': 'Раздел кейса',
                'verbose_name_plural': 'Разделы кейса',
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('Period_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Period_Name', models.CharField(max_length=100, verbose_name='Период')),
                ('Period_Sort', models.FloatField(default=models.AutoField(primary_key=True, serialize=False), null=True, verbose_name='Вес при сортировке')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.case')),
            ],
            options={
                'verbose_name': 'Период',
                'verbose_name_plural': 'Периоды',
            },
        ),
        migrations.AddField(
            model_name='parameter',
            name='section',
            field=models.ManyToManyField(to='cases.section'),
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('Job_ID', models.AutoField(primary_key=True, serialize=False)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.case')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Статус кейса',
                'verbose_name_plural': 'Статусы кейса',
            },
        ),
        migrations.CreateModel(
            name='Formula',
            fields=[
                ('Formula_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Formula_Name', models.CharField(max_length=100, verbose_name='Формула')),
                ('parameter', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cases.parameter')),
                ('variable', models.ManyToManyField(to='cases.variable')),
            ],
            options={
                'verbose_name': 'Формула',
                'verbose_name_plural': 'Формулы',
            },
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('Data_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Data_Value', models.FloatField(blank=True, default=0, null=True, verbose_name='Значение')),
                ('parameter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.parameter')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.period')),
            ],
            options={
                'verbose_name': 'Значение',
                'verbose_name_plural': 'Значения',
            },
        ),
    ]