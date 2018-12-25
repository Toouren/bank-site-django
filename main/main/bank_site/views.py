from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from .models import User, Company, CardPay, OurBankPay, GetPay
from django.shortcuts import redirect
import io
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os


def return_index(request):
    if auth.get_user(request).get_username():
        username = auth.get_user(request).get_username()
        # print(username)
        user = User.objects.get(login__exact=username)
        company = user.company

        if request.POST:
            if 'card-pay' in request.POST:
                print('in_card_pay')
                pay_info = {'user_initiator': user,
                            'sum': request.POST.get('sum'),
                            'comment': request.POST.get('comment'),
                            'email': request.POST.get('email'),
                            'card_num': request.POST.get('number'),
                            'card_date': request.POST.get('date'),
                            'cvc_card': request.POST.get('cvc')}

                new_card_pay = CardPay(user_initiator=pay_info['user_initiator'],
                                       sum=pay_info['sum'],
                                       comment=pay_info['comment'],
                                       email=pay_info['email'],
                                       card_num=pay_info['card_num'],
                                       card_date=pay_info['card_date'],
                                       cvc_card=pay_info['cvc_card'],
                                       accepted=True)

                new_card_pay.save()
                print('card_pay saved')

            elif 'get-bank-pay' in request.POST:
                print(request.POST)
                print('in_get_bank_pay')
                pay_info = {'user_initiator': user,
                            'requester': request.POST.get('get_requester'),
                            'sum': request.POST.get('get_sum'),
                            'comment': request.POST.get('get_comment'),
                            'bik': request.POST.get('get_bik'),
                            'nds': request.POST.get('nds_input'),
                            'phone': request.POST.get('get_email'),
                            'email': request.POST.get('get_phone')}

                get_pay = GetPay(user_initiator=pay_info['user_initiator'],
                                 requester=pay_info['requester'],
                                 sum=pay_info['sum'],
                                 comment=pay_info['comment'],
                                 bik=pay_info['bik'],
                                 nds=pay_info['nds'],
                                 phone=pay_info['phone'],
                                 email=pay_info['phone'])
                get_pay.save()
                print('our_bank_pay saved')

        elif request.GET:
            if 'our-bank-pay' in request.GET:

                pay_info = {'user_initiator': user,
                            'sum': request.GET.get('our_sum'),
                            'comment': request.GET.get('our_comment'),
                            'bik': request.GET.get('our_bik'),
                            'nds': request.GET.get('nds_input'),
                            'payer': request.GET.get('our_payer')}

                new_our_bank_pay = OurBankPay(user_initiator=pay_info['user_initiator'],
                                              sum=pay_info['sum'],
                                              comment=pay_info['comment'],
                                              bik=pay_info['bik'],
                                              nds=pay_info['nds'],
                                              payer=pay_info['payer'])
                new_our_bank_pay.save()

                buffer = io.BytesIO()
                p = canvas.Canvas(buffer)
                pdfmetrics.registerFont(TTFont('FreeSans', os.path.dirname(os.path.abspath(__file__)) +
                                               '/static/fonts/FreeSans.ttf'))
                p.setFont('FreeSans', 18)
                p.drawString(100, 800, "От кого:            {}".format(pay_info['payer']))
                p.line(100, 790, 500, 790)
                p.drawString(100, 750, "БИК:                {}".format(pay_info['bik']))
                p.line(100, 740, 500, 740)
                p.drawString(100, 700, "За что:             {}".format(pay_info['comment']))
                p.line(100, 690, 500, 690)
                p.drawString(100, 650, "НДС:                {}%".format(pay_info['nds']))
                p.line(100, 640, 500, 640)
                p.drawString(100, 590, "Сумма:              {}".format(pay_info['sum']))
                p.line(100, 580, 500, 580)
                p.showPage()
                p.save()

                # print('our_bank_pay saved')

                response = HttpResponse(content_type="application/pdf")
                response['Content-Disposition'] = 'attachment; filename=pay-info.pdf'
                response.write(buffer.getvalue())
                return response

        superuser = 0
        if auth.get_user(request).is_superuser:
            superuser = 1

        context = {'first_name': user.first_name,
                   'second_name': user.second_name,
                   'phone_number': user.phone_number,
                   'email': user.email,
                   'comp_name': company.company_name,
                   'comp_info': company.company_info,
                   'comp_site': company.company_site,
                   'comp_first_pic': company.company_info_first_pic,
                   'comp_first_cost': company.first_pic_cost,
                   'comp_first_name': company.first_pic_name,
                   'comp_second_pic': company.company_info_second_pic,
                   'comp_second_cost': company.second_pic_cost,
                   'comp_second_name': company.second_pic_name,
                   'comp_third_pic': company.company_info_third_pic,
                   'comp_third_cost': company.third_pic_cost,
                   'comp_third_name': company.third_pic_name,
                   'superuser': superuser}
        return render(request, 'main_templates/index.html', context=context)
    return redirect('/login')


def process_logout(request):
    auth.logout(request)
    return redirect('/')


def return_login_index(request):
    if not auth.get_user(request).is_authenticated:
        if request.POST:
            username = request.POST.get('username', '')
            passwd = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=passwd)
            if user:
                auth.login(request, user)
                return redirect('/')
            else:
                return render(request, 'login_templates/index.html', {'error': 1})
        return render(request, 'login_templates/index.html')
    else:
        return redirect('/')


def return_register_index(request):
    if not auth.get_user(request).is_authenticated:
        if request.POST:
            try:
                Company.objects.get(company_name__exact=request.POST.get('comp-name', ''))
                return render(request, 'registration_templates/index.html', {'error': 1})
            except:
                new_comp_data = {'name': request.POST.get('comp-name'), 'site': request.POST.get('comp-site'),
                                 'info': request.POST.get('comp-info'),
                                 'first-pic': request.POST.get('first-pic'),
                                 'first-cost': request.POST.get('first-cost'),
                                 'first-pic-name': request.POST.get('first-name'),
                                 'second-pic': request.POST.get('second-pic'),
                                 'second-cost': request.POST.get('second-cost'),
                                 'second-pic-name': request.POST.get('second-name'),
                                 'third-pic': request.POST.get('third-pic'),
                                 'third-cost': request.POST.get('third-cost'),
                                 'third-pic-name': request.POST.get('third-name')}
                new_comp = Company(company_name=new_comp_data['name'], company_info=new_comp_data['info'],
                                   company_site=new_comp_data['site'],
                                   company_info_first_pic=new_comp_data['first-pic'],
                                   company_info_second_pic=new_comp_data['second-pic'],
                                   company_info_third_pic=new_comp_data['third-pic'],
                                   first_pic_cost=new_comp_data['first-cost'],
                                   second_pic_cost=new_comp_data['second-cost'],
                                   third_pic_cost=new_comp_data['third-cost'],
                                   first_pic_name=new_comp_data['first-pic-name'],
                                   second_pic_name=new_comp_data['second-pic-name'],
                                   third_pic_name=new_comp_data['third-pic-name'])
                new_comp.save()
                return redirect('/register/user')
        return render(request, 'registration_templates/index.html')
    else:
        return redirect('/')


def return_user_register_index(request):
    if not auth.get_user(request).is_authenticated:
        if request.POST:
            try:
                User.objects.get(company__exact=Company.objects.get(company_name__exact=request.POST.get('comp-name')))
                return render(request, 'user_registration_templates/index.html', {'error': 1})
            except:
                new_user_data = {'login': request.POST.get('login'), 'first_name': request.POST.get('name'),
                                 'second_name': request.POST.get('second-name'), 'company': request.POST.get('comp-name'),
                                 'phone_number': request.POST.get('phone'), 'email': request.POST.get('email'),
                                 'password': request.POST.get('pass')}
                new_user = User(login=new_user_data['login'],
                                first_name=new_user_data['first_name'],
                                second_name=new_user_data['second_name'],
                                company=Company.objects.get(company_name__exact=new_user_data['company']),
                                phone_number=new_user_data['phone_number'],
                                email=new_user_data['email'],
                                password=new_user_data['password'])

                auth.models.User.objects.create_user(username=new_user_data['login'],
                                                     password=new_user_data['password'],
                                                     email=new_user_data['email'])

                new_user.save()
                user = auth.authenticate(username=new_user_data['login'],
                                         password=new_user_data['password'])
                auth.login(request, user)
                return redirect('/')
        else:
            return render(request, 'user_registration_templates/index.html')
    else:
        return redirect('/')


def return_moder_index(request):
    if auth.get_user(request).is_authenticated and auth.get_user(request).is_superuser:
        username = auth.get_user(request).get_username()
        card_payes = CardPay.objects.all()
        internet_bank_payes = OurBankPay.objects.all()
        get_payes = GetPay.objects.all()
        user = User.objects.get(login__exact=username)

        context = {'moder_name': user.first_name,
                   'card_pays': card_payes,
                   'internet_bank_pays': internet_bank_payes,
                   'get_pays': get_payes}
        return render(request, 'moderator_templates/index.html', context)
    return redirect('/')


def process_change(request, id):
    if auth.get_user(request).is_authenticated and auth.get_user(request).is_superuser:
        card_pay = CardPay.objects.get(pay_id__exact=id)
        card_pay.accepted = False
        card_pay.save(update_fields=['accepted'])
        return redirect('/moderator')
    return redirect('/')
