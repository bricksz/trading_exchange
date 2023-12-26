from django.urls import path, include
from .views import (
    OrderView, TradeView, UserProfileView, UserViewSet, TokenView, CompanyView, ExchangeData,
    UserSecuritiesAccountView, EquityListView, UserStockListView, SymbolView, QuoteView, StockListView,

    RandomEndPoint
)
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserViewSet)   # 'api/users/       create user by method: 'POST', body: {username, password}


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', obtain_auth_token),
    path('order/', OrderView.as_view()),
    path('trade/', TradeView.as_view()),
    path('profile/', UserProfileView.as_view()),
    path('token/', TokenView.as_view()),
    path('company/', CompanyView.as_view()),
    path('symbol/', SymbolView.as_view()),
    path('orderbook/', ExchangeData.as_view()),
    path('account/', UserSecuritiesAccountView.as_view()),
    path('equities/', EquityListView.as_view()),
    path('stocks/', UserStockListView.as_view()),
    path('quote/', QuoteView.as_view()),
    path('stock-list/', StockListView.as_view()),
    path('test/', RandomEndPoint.as_view()),

]