# Generated by Django 2.0.2 on 2018-07-17 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('terceros', '0001_initial'),
        ('empresas', '0001_initial'),
        ('habitaciones', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('puntos_venta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BitacoraServicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('habitacion_nombre', models.CharField(blank=True, max_length=300, null=True)),
                ('habitacion_anterior_nombre', models.CharField(blank=True, max_length=300, null=True)),
                ('habitacion_nueva_nombre', models.CharField(blank=True, max_length=300, null=True)),
                ('tiempo_contratado_anterior', models.PositiveIntegerField(blank=True, null=True)),
                ('tiempo_contratado_nuevo', models.PositiveIntegerField(blank=True, null=True)),
                ('tiempo_contratado', models.PositiveIntegerField(blank=True, null=True)),
                ('hora_evento', models.DateTimeField(blank=True, null=True)),
                ('tiempo_minutos_recorridos', models.PositiveIntegerField(blank=True, null=True)),
                ('concepto', models.CharField(max_length=200)),
                ('observacion', models.TextField(null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bitacoras_servicios', to=settings.AUTH_USER_MODEL)),
                ('punto_venta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bitacoras_servicios', to='puntos_venta.PuntoVenta')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('estado', models.IntegerField(choices=[(0, 'Inicio'), (1, 'En Servicio'), (2, 'Terminado'), (3, 'Anulado'), (4, 'Solicitud Anulación')], default=0)),
                ('hora_inicio', models.DateTimeField(blank=True, null=True)),
                ('hora_final', models.DateTimeField(blank=True, null=True)),
                ('hora_final_real', models.DateTimeField(blank=True, null=True)),
                ('hora_anulacion', models.DateTimeField(blank=True, null=True)),
                ('tiempo_minutos', models.PositiveIntegerField(default=0)),
                ('categoria', models.CharField(blank=True, max_length=120, null=True)),
                ('valor_servicio', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('valor_habitacion', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('valor_iva_habitacion', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('observacion_anulacion', models.TextField(blank=True, null=True)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='servicios', to='terceros.Cuenta')),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='servicios', to='empresas.Empresa')),
                ('habitacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='servicios', to='habitaciones.Habitacion')),
                ('servicio_anterior', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='servicio_siguiente', to='servicios.Servicio')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='bitacoraservicio',
            name='servicio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bitacoras_servicio', to='servicios.Servicio'),
        ),
    ]
