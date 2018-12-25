from django.db import models


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    company_info = models.CharField(max_length=1000)

    company_site = models.CharField(max_length=300, default='site_is_not_set')

    company_info_first_pic = models.ImageField(null=True, upload_to='goods_pics/')
    company_info_second_pic = models.ImageField(null=True, upload_to='goods_pics/')
    company_info_third_pic = models.ImageField(null=True, upload_to='goods_pics/')

    first_pic_name = models.CharField(null=True, default='', max_length=100)
    second_pic_name = models.CharField(null=True, default='', max_length=100)
    third_pic_name = models.CharField(null=True, default='', max_length=100)

    first_pic_cost = models.IntegerField(null=True, default=0)
    second_pic_cost = models.IntegerField(null=True, default=0)
    third_pic_cost = models.IntegerField(null=True, default=0)


class User(models.Model):
    login = models.CharField(max_length=15, primary_key=True)
    password = models.CharField(max_length=20)
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, default='number_is_not_set')
    email = models.CharField(max_length=90, default='email_is_not_set')


class CardPay(models.Model):
    pay_id = models.AutoField(primary_key=True)
    user_initiator = models.ForeignKey(User, on_delete=models.CASCADE)
    sum = models.IntegerField(null=False)
    comment = models.CharField(max_length=150)
    email = models.EmailField(max_length=90)
    card_num = models.CharField(max_length=16)
    card_date = models.CharField(max_length=5)
    cvc_card = models.CharField(max_length=3)
    accepted = models.BooleanField(default=True)


class OurBankPay(models.Model):
    pay_id = models.AutoField(primary_key=True)
    user_initiator = models.ForeignKey(User, on_delete=models.CASCADE)
    payer = models.CharField(max_length=100)
    bik = models.IntegerField(null=False)
    comment = models.CharField(max_length=150)
    nds = models.IntegerField(null=False)
    sum = models.IntegerField(null=False)


class GetPay(models.Model):
    request_id = models.AutoField(primary_key=True)
    user_initiator = models.ForeignKey(User, on_delete=models.CASCADE)
    requester = models.CharField(max_length=100)
    bik = models.IntegerField(null=False)
    comment = models.CharField(max_length=150)
    nds = models.IntegerField(null=False)
    sum = models.IntegerField(null=False)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=90)
