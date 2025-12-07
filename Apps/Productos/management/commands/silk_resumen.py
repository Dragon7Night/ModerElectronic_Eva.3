from django.core.management.base import BaseCommand
from django.db.models import Avg, Max, Count
from silk.models import Request  # usa los modelos de django-silk


""" 

Comando para mostrar un resumen de las peticiones registradas por django-silk

Ejemplo:
    python manage.py silk_resumen --limit 30

|> --limit : número de rutas (paths) a mostrar en el resumen

"""


class Command(BaseCommand):
    help = "Muestra un resumen de las peticiones registradas por django-silk"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=20,
            help="Número de rutas (paths) a mostrar en el resumen",
        )

    def handle(self, *args, **options):
        limit = options["limit"]

        total = Request.objects.count()

        # === Encabezado bonito ===
        title = " RESUMEN DE PETICIONES DJANGO-SILK "
        border = "=" * len(title)
        self.stdout.write(self.style.MIGRATE_HEADING(border))
        self.stdout.write(self.style.MIGRATE_HEADING(title))
        self.stdout.write(self.style.MIGRATE_HEADING(border))
        self.stdout.write(
            self.style.HTTP_INFO(f"Total de peticiones registradas por Silk: {total}")
        )
        self.stdout.write(self.style.HTTP_INFO(f"Mostrando top {limit} rutas.\n"))

        qs = (
            Request.objects
            .values("method", "path")
            .annotate(
                n=Count("id"),
                avg_time=Avg("time_taken"),        # segundos
                max_time=Max("time_taken"),        # segundos
                avg_queries=Avg("num_sql_queries"),
            )
            .order_by("-n")[:limit]
        )

        if not qs:
            self.stdout.write(self.style.WARNING("No hay peticiones registradas aún."))
            return

        # === Tabla ===
        # Anchos de columna
        w_method = 7
        w_path = 50
        w_reqs = 7
        w_avg_s = 8
        w_avg_ms = 9
        w_max_s = 8
        w_max_ms = 9
        w_sql = 10

        header_border = (
            "+" + "-" * (w_method + 2)
            + "+" + "-" * (w_path + 2)
            + "+" + "-" * (w_reqs + 2)
            + "+" + "-" * (w_avg_s + 2)
            + "+" + "-" * (w_avg_ms + 2)
            + "+" + "-" * (w_max_s + 2)
            + "+" + "-" * (w_max_ms + 2)
            + "+" + "-" * (w_sql + 2)
            + "+"
        )

        header = (
            f"| {'Método':<{w_method}} "
            f"| {'Ruta':<{w_path}} "
            f"| {'Petic.':>{w_reqs}} "
            f"| {'Prom s':>{w_avg_s}} "
            f"| {'Prom ms':>{w_avg_ms}} "
            f"| {'Máx s':>{w_max_s}} "
            f"| {'Máx ms':>{w_max_ms}} "
            f"| {'SQL prom.':>{w_sql}} |"
        )

        self.stdout.write(self.style.HTTP_INFO(header_border))
        self.stdout.write(self.style.HTTP_INFO(header))
        self.stdout.write(self.style.HTTP_INFO(header_border))

        for r in qs:
            method = r["method"] or ""
            path = r["path"] or ""
            n = r["n"] or 0
            avg_time = r["avg_time"] or 0.0   # segundos
            max_time = r["max_time"] or 0.0   # segundos
            avg_queries = r["avg_queries"] or 0.0

            # Convertir a milisegundos
            avg_ms = avg_time * 1000.0
            max_ms = max_time * 1000.0

            # Truncar ruta si es muy larga
            if len(path) > w_path:
                path_display = path[: w_path - 3] + "..."
            else:
                path_display = path

            line = (
                f"| {method:<{w_method}} "
                f"| {path_display:<{w_path}} "
                f"| {n:>{w_reqs}} "
                f"| {avg_time:>{w_avg_s}.3f} "
                f"| {avg_ms:>{w_avg_ms}.1f} "
                f"| {max_time:>{w_max_s}.3f} "
                f"| {max_ms:>{w_max_ms}.1f} "
                f"| {avg_queries:>{w_sql}.2f} |"
            )

            # Resaltar en amarillo las rutas con tiempo promedio > 1s
            if avg_time > 1.0:
                self.stdout.write(self.style.WARNING(line))
            else:
                self.stdout.write(line)

        self.stdout.write(self.style.HTTP_INFO(header_border))
        self.stdout.write(
            self.style.HTTP_INFO(
                "\n* Tiempos en segundos (s) y milisegundos (ms). "
                "'SQL prom.' = promedio de consultas SQL por petición."
            )
        )
