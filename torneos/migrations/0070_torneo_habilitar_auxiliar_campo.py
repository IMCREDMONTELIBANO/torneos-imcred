from django.db import migrations, models
from django.db.models import Q


def activar_en_torneos_con_auxiliares(apps, schema_editor):
    Torneo = apps.get_model("torneos", "Torneo")
    Equipo = apps.get_model("torneos", "Equipo")
    torneo_ids = Equipo.objects.filter(
        (Q(auxiliar_campo__isnull=False) & ~Q(auxiliar_campo=""))
        | (Q(cedula_ac__isnull=False) & ~Q(cedula_ac=""))
        | (Q(telefono_ac__isnull=False) & ~Q(telefono_ac=""))
    ).values_list("categoria__torneo_id", flat=True)
    Torneo.objects.filter(id__in=torneo_ids).update(habilitar_auxiliar_campo=True)


class Migration(migrations.Migration):
    dependencies = [
        ("torneos", "0069_equipo_cedulas_cuerpo_tecnico_ac"),
    ]

    operations = [
        migrations.AddField(
            model_name="torneo",
            name="habilitar_auxiliar_campo",
            field=models.BooleanField(
                default=False,
                help_text="Activa esta opción para mostrar y permitir registrar el auxiliar de campo de cada equipo.",
                verbose_name="Este torneo utiliza auxiliares de campo",
            ),
        ),
        migrations.RunPython(activar_en_torneos_con_auxiliares, migrations.RunPython.noop),
    ]
