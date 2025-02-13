from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Sector(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Classification(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Stock(models.Model):
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=10, unique=True)
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.ticker})"

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="Main Wallet")
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet - {self.name}"

class UserFollowWallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)

class StockInWallet(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    total = models.IntegerField(default=0)


class BuyHistory(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    stock_in_wallet = models.ForeignKey(StockInWallet, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()
    date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f"Purchase of {self.quantity} units of {self.stock_in_wallet.stock.name} at {self.price}"

class SellHistory(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    stock_in_wallet = models.ForeignKey(StockInWallet, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()
    date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f"Selling {self.quantity} units of {self.stock_in_wallet.stock.name} at {self.price}"