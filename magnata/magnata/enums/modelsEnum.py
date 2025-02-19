from django.db import models

class WalletType(models.TextChoices):
    BRASILEIRA = "Brasileira", "Brasileira"
    CRIPTO = "Cripto", "Cripto"
    INTERNACIONAL = "Internacional", "Internacional"
