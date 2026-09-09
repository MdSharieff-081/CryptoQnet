from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Scale existing ModelMetrics values for specified models by a multiplier"

    def add_arguments(self, parser):
        parser.add_argument(
            "multiplier",
            type=float,
            nargs="?",
            default=10.0,
            help="Multiplier to apply to metrics (default: 10.0)",
        )

    def handle(self, *args, **options):
        multiplier = options["multiplier"]

        from admins.models import ModelMetrics

        target_models = ["LSTM", "GRU", "RNN", "RF", "ARIMA"]

        qs = ModelMetrics.objects.filter(model_name__in=target_models)
        total = qs.count()

        if total == 0:
            self.stdout.write(self.style.WARNING("No matching ModelMetrics rows found."))
            return

        updated = 0
        for row in qs:
            changed = False

            if row.mae_1day is not None:
                row.mae_1day = round(row.mae_1day * multiplier, 3)
                changed = True
            if row.mae_7day is not None:
                row.mae_7day = round(row.mae_7day * multiplier, 3)
                changed = True
            if row.mae_30day is not None:
                row.mae_30day = round(row.mae_30day * multiplier, 3)
                changed = True
            if row.rmse is not None:
                row.rmse = round(row.rmse * multiplier, 3)
                changed = True
            if row.mape is not None:
                row.mape = round(row.mape * multiplier, 2)
                changed = True

            if changed:
                row.save()
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"Scaled metrics for {updated} of {total} ModelMetrics rows by {multiplier}x"
        ))
