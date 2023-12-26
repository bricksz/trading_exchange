from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .models import (
    Order, Trade, UserProfile, Company, StockHiddenAttribute, UserSecuritiesAccount, Equity
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password'
        ]

        # Settings to hide password
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True,
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)   # creates user with hashed password
        user_profile = UserProfile.objects.create(user=user)
        Token.objects.create(user=user)
        UserSecuritiesAccount.objects.create(user=user, type="C", cash_balance=50000)
        return user


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = "__all__"


class PostTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    class Meta:
        model = Token
        fields = [
            'username'
        ]

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'email',
            'birth_date',
            'trading_level',
        ]


class UserSecuritiesAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSecuritiesAccount
        fields = '__all__'


class PostUserSecuritiesAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSecuritiesAccount
        fields = [
            'type',
            'cash_balance'
        ]


class CompanySerializer(serializers.ModelSerializer):
    rand_norm_mean = serializers.FloatField(required=False)
    rand_norm_std = serializers.FloatField(required=False)
    market_cap = serializers.IntegerField(required=False)

    class Meta:
        model = Company
        fields = [
            'name',
            'description',
            'shares_outstanding',
            'symbol',
            'quote',
            'active',
            'rand_norm_mean',
            'rand_norm_std',
            'market_cap'
        ]


class CompanyAttributeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=5, required=True)

    class Meta:
        model = StockHiddenAttribute
        fields = [
            'name',
            'rand_norm_mean',
            'rand_norm_std',
            'market_cap'
        ]


class QuoteSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(max_length=5, required=True)

    class Meta:
        model = Company
        fields = [
            'symbol',
            'quote'
        ]


class GetOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'symbol',
            'order_type',
            'instruction',
            'quantity',
            'remainder',
            'price',
            'status',
            'epoch_time_micro',
        ]


class PostOrderSerializer(serializers.ModelSerializer):
    price = serializers.FloatField(required=False)

    class Meta:
        model = Order
        fields = [
            'symbol',
            'order_type',
            'instruction',
            'quantity',
            'price',
        ]

class DeleteOrderSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(required=True)

    class Meta:
        model = Order
        fields = [
            'order_id'
        ]

class GetTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = [
            'id',
            'incoming_order_id',
            'book_order_id',
            'symbol',
            'instruction',
            'quantity',
            'price',
            'timestamp',
        ]



class PostTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = [
            'incoming_order_id',
            'book_order_id',
            'symbol',
            'instruction',
            'quantity',
            'price',
            'timestamp'
        ]

class PostExchangeDataSerializer(serializers.Serializer):
    symbol = serializers.CharField(max_length=5, required=True)

class EquitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Equity
        fields = '__all__'