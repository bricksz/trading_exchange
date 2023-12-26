from django.contrib import admin
from .models import (
    Order, Trade, UserProfile, Company, StockHiddenAttribute,
    Equity, UserSecuritiesAccount,
    # MapEquityToUserSecuritiesAccount,
)

class PositionInline(admin.TabularInline):
    model = Equity
    extra = 9

class UserSecuritiesAccountAdmin(admin.ModelAdmin):
    inlines = (PositionInline, )

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(Trade)
admin.site.register(Company)
admin.site.register(StockHiddenAttribute)
admin.site.register(Equity)
admin.site.register(UserSecuritiesAccount, UserSecuritiesAccountAdmin)

