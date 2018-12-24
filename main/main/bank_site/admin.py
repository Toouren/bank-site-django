from django.contrib import admin
from .models import Company, User, CardPay, OurBankPay, GetPay


admin.site.register(Company)
admin.site.register(User)
admin.site.register(CardPay)
admin.site.register(OurBankPay)
admin.site.register(GetPay)
# Register your models here.
