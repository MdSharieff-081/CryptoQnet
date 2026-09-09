from django.db import models

# Create your models here.
# Create your models here.
class AdminOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)



class Dataset(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='dataset/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ModelMetrics(models.Model):

    MODEL_CHOICES = (
        ('LSTM', 'LSTM'),
        ('GRU', 'GRU'),
        ('RF', 'Random Forest'),
        ('CNN', 'CNN'),
        ('ARIMA', 'ARIMA'),
        ('QSVM', 'QSVM'),
        ('QML', 'QML'),
    )

    COIN_CHOICES = (
        ('Bitcoin', 'Bitcoin'),
        ('Ethereum', 'Ethereum'),
    )

    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    coin_type = models.CharField(
    max_length=20,
    choices=COIN_CHOICES,
    null=True,
    blank=True
    )

    model_name = models.CharField(max_length=50, choices=MODEL_CHOICES)

    mae_1day = models.FloatField(null=True, blank=True)
    mae_7day = models.FloatField(null=True, blank=True)
    mae_30day = models.FloatField(null=True, blank=True)

    rmse = models.FloatField(null=True, blank=True)
    mape = models.FloatField(null=True, blank=True)

    accuracy = models.FloatField(null=True, blank=True)

    trained_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('coin_type', 'model_name')

    def __str__(self):
        return f"{self.coin_type} - {self.model_name}"

