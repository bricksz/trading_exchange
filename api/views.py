from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token
from django.db import transaction

from match_engine.amqp import AMQP

from .serializers import (
    UserSerializer, ProfileSerializer, TokenSerializer, PostTokenSerializer,
    CompanySerializer, CompanyAttributeSerializer, QuoteSerializer,
    PostExchangeDataSerializer,
    UserSecuritiesAccountSerializer, PostUserSecuritiesAccountSerializer,
    EquitySerializer,
    PostOrderSerializer, GetOrderSerializer, DeleteOrderSerializer,
    GetTradeSerializer, PostTradeSerializer
)
from .models import (
    Order, Trade, UserProfile, Company, StockHiddenAttribute,
    UserSecuritiesAccount, Equity,
)
from .utils import admin_view

import time
import traceback
import json
from random import getrandbits
from operator import itemgetter


class UserViewSet(ModelViewSet):
    """
        Using DRF default class ModelViewSet (POST, GET enabled)
        POST request to /api/users/ creates user. See serializers.UserSerializer
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

@admin_view
class TokenView(APIView):
    serializer_class = PostTokenSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get('username')
            try:
                user = User.objects.get(username=username)
                Token.objects.get(user=user).delete()
                new_token = Token.objects.create(user=user)
                return Response(TokenSerializer(new_token).data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"not found": "UserProfile"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"bad request": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get('username')
            try:
                user = User.objects.get(username=username)
                Token.objects.get(user=user).delete()
                return Response({"Message": f"{username} Token Deleted"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"not found": "UserProfile"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"bad request": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):
        user = request.user
        user_profile = UserProfile.objects.filter(user=user)            # For performance: .select_related('user')
        if user_profile.exists():
            return Response(ProfileSerializer(user_profile[0]).data, status=status.HTTP_200_OK)
        return Response({"not found": "UserProfile"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        """ Created upon new user, see: UserSerializer
        """
        pass

    def patch(self, request, format=None):
        """ Updating only specific fields
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            email = serializer.data.get('email')
            birth_date = serializer.data.get('birth_date')
            trading_level = serializer.data.get('trading_level')

            user_profile = UserProfile.objects.filter(user=user)
            if user_profile.exists():
                user_profile = user_profile[0]
                user_profile.email = email
                user_profile.birth_date = birth_date
                user_profile.trading_level = trading_level
                user_profile.save(update_fields=['email', 'birth_date', 'trading_level'])
                return Response(ProfileSerializer(user_profile).data, status=status.HTTP_200_OK)
            return Response({"not found": "UserProfile"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"bad request": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


class UserSecuritiesAccountView(APIView):
    serializer_class = PostUserSecuritiesAccountSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):
        user = request.user
        qs_usa = UserSecuritiesAccount.objects.filter(user=user)
        if qs_usa.exists():
            return Response(UserSecuritiesAccountSerializer(qs_usa[0]).data, status=status.HTTP_200_OK)
        return Response({"not found": "UserSecuritiesAccount"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            account_type = serializer.data.get('type', None)
            cash_balance = serializer.data.get('cash_balance', None)

            user = request.user
            qs_usa = UserSecuritiesAccount.objects.filter(user=user)
            if not qs_usa.exists():
                account_type = account_type or "C"
                cash_balance = cash_balance or 50000
                usa = UserSecuritiesAccount.objects.create(user=user, type=account_type, cash_balance=cash_balance)
                return Response(UserSecuritiesAccountSerializer(usa).data, status=status.HTTP_200_OK)
            else:
                update_fields = []
                if account_type:
                    update_fields.append('type')
                if cash_balance:
                    update_fields.append('cash_balance')
                usa = qs_usa[0]
                usa.type = account_type
                usa.cash_balance = cash_balance
                usa.save(update_fields=update_fields)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"bad request": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

@admin_view
class CompanyView(APIView):
    serializer_class = CompanySerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, format=None):
        company = Company.objects.all()
        return Response(CompanySerializer(company, many=True).data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            description = serializer.data.get('description', "")
            shares_outstanding = serializer.data.get('shares_outstanding', 300000000)
            symbol = serializer.data.get('symbol')
            quote = serializer.data.get('quote', None)
            active = serializer.data.get('active', False)

            rand_norm_mean = serializer.data.get('rand_norm_mean', 0.0)
            rand_norm_std = serializer.data.get('rand_norm_std', 1.0)
            market_cap = serializer.data.get('market_cap', None)

            company, _ = Company.objects.update_or_create(
                name=name,
                description=description,
                shares_outstanding=shares_outstanding,
                symbol=str(symbol).upper(),
                quote=quote,
                active=active,
            )

            sha, _ = StockHiddenAttribute.objects.update_or_create(
                company=company,
                rand_norm_mean=rand_norm_mean,
                rand_norm_std=rand_norm_std,
                market_cap=market_cap
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"bad request": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            description = serializer.data.get('description')
            shares_outstanding = serializer.data.get('shares_outstanding')
            symbol = serializer.data.get('symbol')
            quote = serializer.data.get('quote')
            active = serializer.data.get('active')

            company, _ = Company.objects.update_or_create(
                name=name,
                description=description,
                shares_outstanding=shares_outstanding,
                symbol=str(symbol).upper(),
                quote=quote,
                active=active,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"bad request": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

@admin_view
class CompanyAttributeView(APIView):
    serializer_class = CompanyAttributeSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, format=None):
        company = Company.objects.all()
        return Response(CompanyAttributeSerializer(company, many=True).data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            symbol = serializer.data.get('symbol')
            rand_norm_mean = serializer.data.get('rand_norm_mean', 0.0)
            rand_norm_std = serializer.data.get('rand_norm_std', 1.0)
            market_cap = serializer.data.get('market_cap', None)

            company = Company.objects.filter(symbol=symbol)
            if not company.exists():
                return Response(
                    {"bad request": f"symbol {symbol} does not exist."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            sha, _ = StockHiddenAttribute.objects.update_or_create(
                company=company[0],
                rand_norm_mean=rand_norm_mean,
                rand_norm_std=rand_norm_std,
                market_cap=market_cap
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"bad request": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

@admin_view
class QuoteView(APIView):
    serializer_class = QuoteSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            symbol = serializer.data.get('symbol')
            quote = serializer.data.get('quote')

            company = Company.objects.filter(symbol=symbol)
            if company.exists():
                company = company[0]
                company.quote = None if quote == 0.0 else quote
                company.save(update_fields=['quote'])
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"bad request": f"Symbol does not exist: {symbol}"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"bad request": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

class SymbolView(APIView):
    serializer_class = CompanySerializer

    def get(self, request, format=None):
        symbol = self.request.query_params.get("symbol", None)
        if symbol:
            stock = Company.objects.filter(symbol=symbol)
            if stock.exists():
                return Response(CompanySerializer(stock[0]).data, status=status.HTTP_200_OK)
            return Response({"bad request": f"Symbol does not exist: {symbol}"}, status=status.HTTP_404_NOT_FOUND)
        company = Company.objects.all()
        return Response(CompanySerializer(company, many=True).data, status=status.HTTP_200_OK)


@admin_view
class ExchangeData(APIView):
    post_serializer_class = PostExchangeDataSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, format=None):
        serializer = self.post_serializer_class(data=request.data)
        if serializer.is_valid():
            amqp = AMQP()

            symbol = serializer.data.get('symbol', None)

            company = Company.objects.filter(symbol=symbol)
            if not company.exists():
                return Response(
                    {"bad request": f"symbol {symbol} does not exist."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            inital_symbol = symbol[0].lower()
            exchange_name = f"orderbook_{inital_symbol}"
            routing_key = f"exchange.orderbook.{inital_symbol}"

            payload = {'exchange': {'symbol': symbol}}

            if not amqp.connection_status():
                amqp.reconnect()
            try:
                channel = amqp.channel
                channel.exchange_declare(exchange=exchange_name, exchange_type='topic')
                channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=json.dumps(payload))
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                amqp.reconnect()
                channel = amqp.channel
                channel.exchange_declare(exchange=exchange_name, exchange_type='topic')
                channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=json.dumps(payload))

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"bad request": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

class OrderView(APIView):
    """
        body = {
            'symbol': 'AAAA',
            'order_type': 'MKT',    # ['MKT', 'LMT', 'CNL']
            'instruction': 'BUY',   # ['BUY', 'SELL']
            'quantity': 100,
            'price': 30.25,         # Must include if LIMIT order
        }
    """
    post_serializer_class = PostOrderSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):
        order_id = self.request.query_params.get("order_id", None)
        status = self.request.query_params.get("status", None)      # status will be skipped if order_id is provided

        user = request.user
        user_securities_account = UserSecuritiesAccount.objects.filter(user=user)
        if not user_securities_account.exists():
            return Response(
                {"bad request": f"No active securities account for {user.username}."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if order_id is None:
            if status:
                orders = Order.objects.filter(user_securities_account=user_securities_account[0], status=status)
            else:
                orders = Order.objects.filter(user_securities_account=user_securities_account[0])
            return Response(GetOrderSerializer(orders, many=True).data, status=status.HTTP_200_OK)

        order = Order.objects.filter(user_securities_account=user_securities_account[0], id=order_id)
        if order.exists():
            return Response(GetOrderSerializer(order[0], many=False).data, status=status.HTTP_200_OK)
        return Response({"not found": f"Order_id {order_id}"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        serializer = self.post_serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            amqp = AMQP()

            symbol = serializer.data.get('symbol')
            order_type = serializer.data.get('order_type')
            instruction = serializer.data.get('instruction')
            quantity = serializer.data.get('quantity')

            user = request.user
            user_securities_account = UserSecuritiesAccount.objects.filter(user=user)
            if not user_securities_account.exists():
                return Response(
                    {"bad request": f"No active securities account for {user.username}."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            company = Company.objects.filter(symbol=symbol).only('symbol', 'active')
            if not company.exists():
                return Response(
                    {"bad request": f"Symbol {symbol} does not exist."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not company[0].active:
                return Response(
                    {"bad request": f"Symbol {symbol} is not active."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            price = serializer.data.get('price', None)
            if order_type in ["LMT"]:
                if price is None:
                    return Response(
                        {"bad request": f"Limit orders must be accompanied with 'price' field"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                elif price <= 0:
                    return Response(
                        {"bad request": f"Price must be higher than 0.0"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            order = Order.objects.create(
                user_securities_account=user_securities_account[0],
                symbol=symbol,
                order_type=order_type,
                instruction=instruction,
                quantity=quantity,
                remainder=quantity,
                price=price
            )
            inital_symbol = symbol[0].lower()
            exchange_name = f"orderbook_{inital_symbol}"
            routing_key = f"exchange.orderbook.{inital_symbol}"
            payload = {
                'order': {
                    'user_securities_account_id': user_securities_account[0].id,
                    'symbol': symbol,
                    'order_type': order_type,
                    'order_id': int(order.id),
                    'instruction': instruction,
                    'quantity': quantity,
                    'price': price
                }
            }
            if not amqp.connection_status():
                amqp.reconnect()
            try:
                channel = amqp.channel
                channel.exchange_declare(exchange=exchange_name, exchange_type='topic')
                channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=json.dumps(payload))
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                amqp.reconnect()
                channel = amqp.channel
                channel.exchange_declare(exchange=exchange_name, exchange_type='topic')
                channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=json.dumps(payload))
            return Response(GetOrderSerializer(order, many=False).data, status=status.HTTP_200_OK)
        return Response({"bad request": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        pass

    def delete(self, request, format=None):
        """ Cancel order
        """
        serializer = DeleteOrderSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            amqp = AMQP()

            order_id = serializer.data.get('order_id')

            user = request.user
            user_securities_account = UserSecuritiesAccount.objects.filter(user=user)
            if not user_securities_account.exists():
                return Response(
                    {"bad request": f"No active securities account for {user.username}."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            qs_order = Order.objects.filter(user_securities_account=user_securities_account[0], id=order_id)
            if qs_order.exists():
                order = qs_order[0]
                symbol = order.symbol

                payload = {
                    'order': {
                        'user_securities_account_id': user_securities_account[0].id,
                        'symbol': symbol,
                        'order_type': "CNL",
                        'order_id': int(order_id),
                        'instruction': "BUY" if bool(getrandbits(1)) else "SELL",
                        'quantity': 1,
                        'price': 1
                    }
                }

                inital_symbol = symbol[0].lower()
                exchange_name = f"orderbook_{inital_symbol}"
                routing_key = f"exchange.orderbook.{inital_symbol}"

                if not amqp.connection_status():
                    amqp.reconnect(True)
                try:
                    channel = amqp.channel
                    channel.exchange_declare(exchange=exchange_name, exchange_type='topic')
                    channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=json.dumps(payload))
                except Exception as e:
                    traceback.print_exception(type(e), e, e.__traceback__)
                    amqp.reconnect(True)
                    channel = amqp.channel
                    channel.exchange_declare(exchange=exchange_name, exchange_type='topic')
                    channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=json.dumps(payload))

                order.delete()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"not found": f"Order_id {order_id}"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"bad request": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


class TradeView(APIView):
    post_serializer_class = PostTradeSerializer

    def get(self, request, format=None):
        trade_id = self.request.query_params.get("trade_id", None)
        if trade_id is None:
            trade = Trade.objects.all()
            return Response(GetTradeSerializer(trade, many=True).data, status=status.HTTP_200_OK)
        trade = Trade.objects.filter(id=trade_id)
        if trade.exists():
            return Response(GetTradeSerializer(trade, many=False).data, status=status.HTTP_200_OK)
        return Response({"not found": f"Order_id {trade_id}"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        serializer = self.post_serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            incoming_order_id = serializer.data.get('incoming_order_id')
            book_order_id = serializer.data.get('book_order_id')
            symbol = serializer.data.get('symbol')
            instruction = serializer.data.get('instruction')
            quantity = serializer.data.get('quantity')
            price = serializer.data.get('price')
            timestamp = serializer.data.get('timestamp')

            trade = Trade.objects.create(
                incoming_order_id=incoming_order_id,
                book_order_id=book_order_id,
                symbol=symbol,
                instruction=instruction,
                quantity=quantity,
                price=price,
                timestamp=timestamp
            )

            # For incoming user if existing
            qs_order = Order.objects.filter(id=trade.incoming_order_id)
            if qs_order.exists():
                incoming_order = qs_order[0]
                incoming_order.remainder -= quantity
                if (book_order_id < 0) or (incoming_order.remainder <= 0):
                    incoming_order.status = "COMPLETE"
                incoming_order.save(update_fields=['remainder', 'status'])

                # incoming_user_securities_account = UserSecuritiesAccount.objects.filter(
                #     id=incoming_order.user_securities_account_id)

                # optimistic concurrency
                incoming_user_securities_account = UserSecuritiesAccount.objects.select_for_update().filter(
                    id=incoming_order.user_securities_account_id)
                with transaction.atomic():
                    if incoming_user_securities_account.exists():
                        usa = incoming_user_securities_account[0]

                        direction = 1 if instruction == "BUY" else -1
                        quantity_direction = quantity * direction
                        trade_basis =  quantity_direction * price

                        # Saving to equity positions
                        qs_equity = usa.equity.filter(symbol=symbol)
                        if qs_equity:
                            equity = qs_equity[0]
                            sign_difference = (equity.quantity * (equity.quantity + quantity_direction)) < 0
                            cost_basis = equity.quantity * equity.basis
                            equity.quantity += quantity_direction
                            if equity.quantity != 0:
                                if sign_difference:
                                    equity.basis = price
                                else:
                                    if abs(cost_basis) < abs(cost_basis + trade_basis):
                                        equity.basis = ((cost_basis + trade_basis) / equity.quantity)
                                equity.save(update_fields=['quantity', 'basis'])
                            else:
                                equity.delete()
                        else:
                            usa.equity.create(symbol=symbol, quantity=(quantity*direction), basis=price, user_securities_account=usa.id)
                        usa.cash_balance -= trade_basis
                        usa.save()

            # For book user if existing
            qs_order = Order.objects.filter(id=trade.book_order_id)
            if qs_order.exists():
                book_order = qs_order[0]
                book_order.remainder -= quantity
                if (book_order_id < 0) or (book_order.remainder <= 0):
                    book_order.status = "COMPLETE"
                book_order.save(update_fields=['remainder', 'status'])

                # book_user_securities_account = UserSecuritiesAccount.objects.filter(
                #     id=book_order.user_securities_account_id)

                # optimistic concurrency
                book_user_securities_account = UserSecuritiesAccount.objects.select_for_update().filter(
                    id=book_order.user_securities_account_id)
                with transaction.atomic():
                    if book_user_securities_account.exists():
                        busa = book_user_securities_account[0]

                        direction = -1 if instruction == "BUY" else 1
                        quantity_direction = quantity * direction
                        trade_basis =  quantity_direction * price

                        # Saving to equity positions
                        qs_equity = busa.equity.filter(symbol=symbol)
                        if qs_equity:
                            equity = qs_equity[0]
                            sign_difference = (equity.quantity * (equity.quantity + quantity_direction)) < 0
                            cost_basis = equity.quantity * equity.basis
                            equity.quantity += quantity_direction
                            if equity.quantity != 0:
                                if sign_difference:
                                    equity.basis = price
                                else:
                                    if abs(cost_basis) < abs(cost_basis + trade_basis):
                                        equity.basis = ((cost_basis + trade_basis) / equity.quantity)
                                equity.save()
                            else:
                                equity.delete()
                        else:
                            busa.equity.create(symbol=symbol, quantity=(quantity*direction), basis=price, user_securities_account_id=busa.id)
                        busa.cash_balance -= trade_basis
                        busa.save()

            qs_company = Company.objects.filter(symbol=symbol)
            if qs_company.exists():
                company = qs_company[0]
                company.quote = None if price == 0.0 else price
                company.save(update_fields=['quote'])

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"bad request": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, format=None):
        pass

    def delete(self, request, format=None):
        pass

class EquityListView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):
        symbol = self.request.query_params.get("symbol", None)
        user = request.user
        qs_usa = UserSecuritiesAccount.objects.filter(user=user)
        if qs_usa.exists():
            if symbol:
                equities = Equity.objects.filter(user_securities_account_id=qs_usa[0].id, symbol=symbol)
                if not equities.exists():
                    return Response({"bad request": f"Symbol does not exist in UserSecuritiesAccount: {symbol}"},
                                    status=status.HTTP_404_NOT_FOUND)
                return Response(EquitySerializer(equities[0]).data, status=status.HTTP_200_OK)

            equities = Equity.objects.filter(user_securities_account_id= qs_usa[0].id)
            return Response(EquitySerializer(equities, many=True).data, status=status.HTTP_200_OK)
        return Response({"bad request": ""}, status=status.HTTP_404_NOT_FOUND)


class StockListView(APIView):
    def get(self, request, format=None):
        stocks = Company.objects.filter(active=True)
        return Response(CompanySerializer(stocks, many=True).data, status=status.HTTP_200_OK)

class UserStockListView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):
        user = request.user
        qs_usa = UserSecuritiesAccount.objects.filter(user=user)
        if qs_usa.exists():
            equities = Equity.objects.filter(user_securities_account_id= qs_usa[0].id)
            if equities.exists():
                symbols = equities.values_list('symbol', flat=True)
                stocks = Company.objects.filter(symbol__in=symbols)
                return Response(CompanySerializer(stocks, many=True).data, status=status.HTTP_200_OK)
            return Response([], status.HTTP_200_OK)
        return Response({"not found": "UserSecuritiesAccount"}, status=status.HTTP_404_NOT_FOUND)

class RandomEndPoint(APIView):
    serializer_class = PostTradeSerializer

    def post(self, request, format=None):
        request_data = request.data.get("batch_trades", None)
        is_data_valid = isinstance(request_data, list)
        if not is_data_valid:
            try:
                json_request_data = json.loads(request_data)
            except Exception as e:
                print(f"JSON Exception: {e}")
                return Response({"invalid data": "batch_trades data must be JSON parsable"},
                                status=status.HTTP_404_NOT_FOUND)
            is_json_data_valid = isinstance(json_request_data, list)
            if not is_json_data_valid:
                return Response({"invalid data": "Must be arrays like objects"}, status=status.HTTP_400_BAD_REQUEST)
            request_data = json_request_data

        serializer = self.serializer_class(data=request_data, many=True)
        if serializer.is_valid(raise_exception=True):
            batch_data = serializer.data
            dict_usa_by_id = {}
            dict_orders_by_id = {}
            dict_usa_equity_by_usa_id = {}
            order_ids = list(map(itemgetter('incoming_order_id'), batch_data)) + list(
                map(itemgetter('book_order_id'), batch_data))
            qs_order = Order.objects.select_for_update().filter(id__in=order_ids)

            usa_ids = qs_order.values_list('user_securities_account', flat=True)
            qs_usa = UserSecuritiesAccount.objects.select_for_update().filter(id__in=usa_ids)

            qs_equity = Equity.objects.select_for_update().filter(user_securities_account_id__in=usa_ids)

            with transaction.atomic():
                if not qs_order.exists():
                    return Response({"bad request": "no existing Order objects"}, status=status.HTTP_401_UNAUTHORIZED)
                if not qs_usa.exists():
                    return Response({"bad request": "no existing UserSecuritiesAccount objects"},
                                    status=status.HTTP_402_PAYMENT_REQUIRED)
                if not qs_equity.exists():
                    print('no existing qs_equity!')
                    # return Response({"bad request": "no existing Equity objects"}, status=status.HTTP_403_FORBIDDEN)

                for usa in qs_usa:
                    if usa.id not in dict_usa_by_id:
                        dict_usa_by_id[usa.id] = usa
                for order in qs_order:
                    if order.id not in dict_orders_by_id:
                        dict_orders_by_id[order.id] = order
                for equity in qs_equity:
                    usa_equity_key = f"{equity.user_securities_account_id}_{equity.symbol}"
                    if usa_equity_key not in dict_usa_equity_by_usa_id:
                        dict_usa_equity_by_usa_id[usa_equity_key] = equity

                batch_trades = []
                for d in batch_data:
                    incoming_order_id = d.get('incoming_order_id')
                    book_order_id = d.get('book_order_id')
                    symbol = d.get('symbol')
                    instruction = d.get('instruction')
                    quantity = d.get('quantity')
                    price = d.get('price')
                    timestamp = d.get('timestamp')
                    batch_trades.append(Trade(
                        incoming_order_id=incoming_order_id,
                        book_order_id=book_order_id,
                        symbol=symbol,
                        instruction=instruction,
                        quantity=quantity,
                        price=price,
                        timestamp=timestamp
                    ))

                    ### For incoming user if existing ###
                    incoming_order = dict_orders_by_id.get(incoming_order_id, None)
                    if incoming_order:
                        incoming_order.remainder -= quantity
                        if (book_order_id < 0) or (incoming_order.remainder <= 0):
                            incoming_order.status = "COMPLETE"

                        # optimistic concurrency
                        incoming_usa = dict_usa_by_id.get(incoming_order.user_securities_account_id, None)
                        if incoming_usa:
                            direction = 1 if instruction == "BUY" else -1
                            quantity_direction = quantity * direction
                            trade_basis = quantity_direction * price

                            # Saving to equity positions
                            usa_equity_key = f"{incoming_usa.id}_{symbol}"
                            equity = dict_usa_equity_by_usa_id.get(usa_equity_key, None)
                            if equity:
                                sign_difference = (equity.quantity * (equity.quantity + quantity_direction)) < 0
                                cost_basis = equity.quantity * equity.basis
                                equity.quantity += quantity_direction
                                if equity.quantity != 0:
                                    if sign_difference:
                                        equity.basis = price
                                    else:
                                        if abs(cost_basis) < abs(cost_basis + trade_basis):
                                            equity.basis = ((cost_basis + trade_basis) / equity.quantity)
                                else:
                                    _ = dict_usa_equity_by_usa_id.pop(usa_equity_key, None)
                                    equity.delete()
                            else:
                                dict_usa_equity_by_usa_id[usa_equity_key] = Equity(
                                    symbol=symbol,
                                    quantity=(quantity * direction),
                                    basis=price,
                                    user_securities_account_id=incoming_usa.id
                                )
                            incoming_usa.cash_balance -= trade_basis

                    ### For book user if existing ###
                    book_order = dict_orders_by_id.get(book_order_id, None)
                    if book_order:
                        book_order.remainder -= quantity
                        if (book_order_id < 0) or (book_order.remainder <= 0):
                            book_order.status = "COMPLETE"

                        # optimistic concurrency
                        book_usa = dict_usa_by_id[book_order.user_securities_account_id]
                        if book_usa:
                            direction = -1 if instruction == "BUY" else 1
                            quantity_direction = quantity * direction
                            trade_basis = quantity_direction * price

                            # Saving to equity positions
                            usa_equity_key = f"{book_usa.id}_{symbol}"
                            equity = dict_usa_equity_by_usa_id.get(usa_equity_key, None)
                            if equity:
                                sign_difference = (equity.quantity * (equity.quantity + quantity_direction)) < 0
                                cost_basis = equity.quantity * equity.basis
                                equity.quantity += quantity_direction
                                if equity.quantity != 0:
                                    if sign_difference:
                                        equity.basis = price
                                    else:
                                        if abs(cost_basis) < abs(cost_basis + trade_basis):
                                            equity.basis = ((cost_basis + trade_basis) / equity.quantity)
                                else:
                                    _ = dict_usa_equity_by_usa_id.pop(usa_equity_key, None)
                                    equity.delete()
                            else:
                                dict_usa_equity_by_usa_id[usa_equity_key] = Equity(
                                    symbol=symbol,
                                    quantity=(quantity * direction),
                                    basis=price,
                                    user_securities_account_id=book_usa.id
                                )
                            book_usa.cash_balance -= trade_basis
                # Save all
                # dict_usa_by_id = {}       # UserSecuritiesAccount model objects by id
                # dict_orders_by_id = {}    # Order model objects by id
                # dict_usa_equity_by_usa_id = {}    # Equity model objects by usa_id + equity symbol

                Order.objects.bulk_update([dict_orders_by_id[k] for k in dict_orders_by_id], ['remainder', 'status'])
                UserSecuritiesAccount.objects.bulk_update([dict_usa_by_id[k] for k in dict_usa_by_id], ['cash_balance'])

                existing_equity_ids = Equity.objects.filter(user_securities_account_id__in=usa_ids).select_for_update().values_list('id', flat=True)

                create_equity = [
                    dict_usa_equity_by_usa_id[k] for k in dict_usa_equity_by_usa_id if
                    dict_usa_equity_by_usa_id[k].id not in existing_equity_ids
                ]
                Equity.objects.bulk_create(create_equity)
                Equity.objects.bulk_update([dict_usa_equity_by_usa_id[k] for k in dict_usa_equity_by_usa_id], ['quantity', 'basis'])
                return Response({"batch_trades": f"processed {len(batch_data)} trades"}, status=status.HTTP_200_OK)


                ################################################################
                # for d in batch_data:
                #     incoming_order_id = d.get('incoming_order_id')
                #     book_order_id = d.get('book_order_id')
                #     symbol = d.get('symbol')
                #     instruction = d.get('instruction')
                #     quantity = d.get('quantity')
                #     price = d.get('price')
                #     timestamp = d.get('timestamp')
                #     trade = Trade.objects.create(
                #         incoming_order_id=incoming_order_id,
                #         book_order_id=book_order_id,
                #         symbol=symbol,
                #         instruction=instruction,
                #         quantity=quantity,
                #         price=price,
                #         timestamp=timestamp
                #     )
                #     # For incoming user if existing
                #     qs_order = Order.objects.filter(id=trade.incoming_order_id)
                #     if qs_order.exists():
                #         incoming_order = qs_order[0]
                #         incoming_order.remainder -= quantity
                #         if (book_order_id < 0) or (incoming_order.remainder <= 0):
                #             incoming_order.status = "COMPLETE"
                #         incoming_order.save(update_fields=['remainder', 'status'])
                #
                #         # optimistic concurrency
                #         incoming_user_securities_account = UserSecuritiesAccount.objects.select_for_update().filter(
                #             id=incoming_order.user_securities_account_id)
                #         with transaction.atomic():
                #             if incoming_user_securities_account.exists():
                #                 usa = incoming_user_securities_account[0]
                #
                #                 direction = 1 if instruction == "BUY" else -1
                #                 quantity_direction = quantity * direction
                #                 trade_basis = quantity_direction * price
                #
                #                 # Saving to equity positions
                #                 qs_equity = usa.equity.filter(symbol=symbol)
                #                 if qs_equity:
                #                     equity = qs_equity[0]
                #                     sign_difference = (equity.quantity * (equity.quantity + quantity_direction)) < 0
                #                     cost_basis = equity.quantity * equity.basis
                #                     equity.quantity += quantity_direction
                #                     if equity.quantity != 0:
                #                         if sign_difference:
                #                             equity.basis = price
                #                         else:
                #                             if abs(cost_basis) < abs(cost_basis + trade_basis):
                #                                 equity.basis = ((cost_basis + trade_basis) / equity.quantity)
                #                         equity.save(update_fields=['quantity', 'basis'])
                #                     else:
                #                         equity.delete()
                #                 else:
                #                     usa.equity.create(symbol=symbol, quantity=(quantity * direction), basis=price, user_securities_account_id=usa.id)
                #                 usa.cash_balance -= trade_basis
                #                 usa.save()
                #
                #     # For book user if existing
                #     qs_order = Order.objects.filter(id=trade.book_order_id)
                #     if qs_order.exists():
                #         book_order = qs_order[0]
                #         book_order.remainder -= quantity
                #         if (book_order_id < 0) or (book_order.remainder <= 0):
                #             book_order.status = "COMPLETE"
                #         book_order.save(update_fields=['remainder', 'status'])
                #
                #         # optimistic concurrency
                #         book_user_securities_account = UserSecuritiesAccount.objects.select_for_update().filter(
                #             id=book_order.user_securities_account_id)
                #         with transaction.atomic():
                #             if book_user_securities_account.exists():
                #                 busa = book_user_securities_account[0]
                #
                #                 direction = -1 if instruction == "BUY" else 1
                #                 quantity_direction = quantity * direction
                #                 trade_basis = quantity_direction * price
                #
                #                 # Saving to equity positions
                #                 qs_equity = busa.equity.filter(symbol=symbol)
                #                 if qs_equity:
                #                     equity = qs_equity[0]
                #                     sign_difference = (equity.quantity * (equity.quantity + quantity_direction)) < 0
                #                     cost_basis = equity.quantity * equity.basis
                #                     equity.quantity += quantity_direction
                #                     if equity.quantity != 0:
                #                         if sign_difference:
                #                             equity.basis = price
                #                         else:
                #                             if abs(cost_basis) < abs(cost_basis + trade_basis):
                #                                 equity.basis = ((cost_basis + trade_basis) / equity.quantity)
                #                         equity.save()
                #                     else:
                #                         equity.delete()
                #                 else:
                #                     busa.equity.create(symbol=symbol, quantity=(quantity * direction), basis=price, user_securities_account_id=busa.id)
                #                 busa.cash_balance -= trade_basis
                #                 busa.save()
                #
                # return Response({"batch_trades": f"processed {len(batch_data)} trades"}, status=status.HTTP_200_OK)

        return Response({"bad request": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
