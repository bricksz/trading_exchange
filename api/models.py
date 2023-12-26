from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from time import time

class UserProfile(models.Model):
    TRADING_LEVEL_CHOICES = [
        (1, 'No Experience'),
        (2, 'Beginner'),
        (3, 'Intermediate'),
        (4, 'Advanced'),
        (5, 'Professional'),
    ]

    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    email = models.EmailField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    trading_level = models.PositiveSmallIntegerField(choices=TRADING_LEVEL_CHOICES, null=True)
    date_created = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return f'{self.user.username}'


class Company(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=1000, default="")
    shares_outstanding = models.BigIntegerField(null=False, default=300000000)
    symbol = models.CharField(max_length=5, unique=True, null=False, blank=False)
    quote = models.FloatField(null=True, default=None)

    active = models.BooleanField(null=False, default=False)
    epoch_time_micro = models.BigIntegerField(null=False, default=int(time() * 1e6))

    def __repr__(self):
        return f"({self.symbol}) {self.name}"

    def __str__(self):
        return f"({self.symbol}) {self.name}"


class StockHiddenAttribute(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    rand_norm_mean = models.FloatField(null=False, default=0.0)
    rand_norm_std = models.FloatField(null=False, default=1.0)
    market_cap = models.BigIntegerField(null=True, default=None)
    epoch_time_micro = models.BigIntegerField(null=False, default=int(time() * 1e6))


class UserSecuritiesAccount(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('C', 'CASH'),
        # ('M', 'MARGIN'),
    ]

    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=1, choices=ACCOUNT_TYPE_CHOICES, default='C')
    cash_balance = models.FloatField(default=0.0)
    # equity = models.ManyToManyField(Equity, through='MapEquityToUserSecuritiesAccount')


class Equity(models.Model):
    """
        TODO: adding margin
        if short sale value cannot exceed margin_maintenance * (1 + margin_requirement)
        margin call when approaching or request to deposit more cash.
    """
    symbol = models.CharField(max_length=5)
    quantity = models.BigIntegerField(default=0)
    basis = models.FloatField(default=0.0)
    user_securities_account = models.ForeignKey('UserSecuritiesAccount', on_delete=models.CASCADE)

    def __repr__(self):
        return f"(id: {self.id}) {self.symbol} {self.quantity} Shares at {self.basis}"

    def __str__(self):
        return f"(id: {self.id}) {self.symbol} {self.quantity} Shares at {self.basis}"


# class MapEquityToUserSecuritiesAccount(models.Model):
#     """
#         Maps Equity id to UserSecuritiesAccount id
#     """
#     equity = models.ForeignKey(Equity, on_delete=models.CASCADE)
#     user_securities_account = models.ForeignKey(UserSecuritiesAccount, on_delete=models.CASCADE)


class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('MKT', 'MARKET'),
        ('LMT', 'LIMIT'),
        ('CNL', 'CANCEL'),
    ]
    INSTRUCTION_CHOICES = [
        ('BUY', 'BUY'),
        ('SELL', 'SELL'),
    ]

    user_securities_account = models.ForeignKey(UserSecuritiesAccount, null=True, on_delete=models.SET_NULL)
    symbol = models.CharField(max_length=5)
    order_type = models.CharField(max_length=5, choices=ORDER_TYPE_CHOICES)
    instruction = models.CharField(max_length=5, choices=INSTRUCTION_CHOICES)
    quantity = models.PositiveBigIntegerField(null=False)
    price = models.FloatField(null=True)

    remainder = models.BigIntegerField(null=False)
    status = models.CharField(max_length=100, default="PENDING")
    epoch_time_micro = models.BigIntegerField(null=False, default=int(time()*1e6))


class Trade(models.Model):
    INSTRUCTION_CHOICES = [
        ('BUY', 'BUY'),
        ('SELL', 'SELL'),
    ]

    incoming_order_id = models.BigIntegerField(null=False)
    book_order_id = models.BigIntegerField(null=False)
    symbol = models.CharField(null=False, max_length=5)
    instruction = models.CharField(null=False, max_length=5, choices=INSTRUCTION_CHOICES)
    quantity = models.BigIntegerField(null=False)
    price = models.FloatField(null=False)
    timestamp = models.BigIntegerField(null=False)


