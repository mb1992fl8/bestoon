# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import requests
import random
import string
import time

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from json import JSONEncoder

#from django.contrib.auth import authenticate, login, logout


from django.views.decorators.csrf import csrf_exempt
#from django.views.decorators.http import require_POST
from first.models import User, Token, Expense, Income, Passwordresetcodes
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
#from postmark import PMMail
from django.db.models import Sum, Count

#from .utils import grecaptcha_verify, RateLimited


###################################################################
###################################################################
###################################################################

#-*- coding: utf-8 -*-
#from __future__ import unicode_literals

#from datetime import datetime
#from json import JSONEncoder

#from django.conf import settings
#from django.shortcuts import render, get_object_or_404
#from django.contrib.auth.hashers import make_password
#from django.contrib.auth.models import User
#from django.db.models import Sum, Count
#from django.http import JsonResponse
#from django.shortcuts import render
#from django.utils.crypto import get_random_string
#from django.views.decorators.csrf import csrf_exempt
#from first.models import User, Token, Expense, Income, Passwordresetcodes
#from datetime import datetime
#from django.contrib.auth.hashers import make_password, check_password

#from postmark import PMMail

#from django.db.models import Sum, Count

# Create your views here.
#from postmark import PMMail

#from .models import Token, Expense, Income, Passwordresetcodes
#from .utils import grecaptcha_verify

######################################################################
######################################################################
######################################################################


#Creating random string for Token
random_str = lambda N: ''.join(
    random.SystemRandom().choice(
        string.ascii_uppercase + string.ascii_lowercase + string.digits)\
              for _ in range(N))



#login, (API) , returns : JSON = status (ok|error) and token
@csrf_exempt
def login(request):
    print(request.POST)
    if request.POST.has_key('username') and request.POST.has_key('password'): #check if POST request has username and password
        username = request.POST['username']
        password = request.POST['password']
        this_user = get_object_or_404(User, username=username)
        if (check_password(password, this_user.password)): #authentication
            this_token = get_object_or_404(Token, user=this_user)
            token = this_token.token
            context = {}
            context['result'] = 'ok'
            context['token'] = token
            return JsonResponse (context, encoder=JSONEncoder) #return {'status':'ok', 'token':'TOKEN'}
        else:
            context = {}
            context['result'] = 'error'
            return JsonResponse (context, encoder=JSONEncoder) #return {'status':'error'}


#register (web)
def register(request):
    if request.POST.has_key(
        'requestcode'):  #form is filled. if not spam, 
              #generate code and save in db, 
              #wait for email confirmation, return message
        
        #is this spam? check reCaptcha
        if not grecaptcha_verify(request): # captcha was not correct
            context = {\
                'message': 'کپچای گوگل درست وارد نشده بود. شاید ربات هستید؟\
                    کد یا کلیک یا تشخیص عکس زیر فرم را درست پر کنید.\
                        ببخشید که فرم به شکل اولیه برنگشته!'}
#TODO: forgot password
            return render(request, 'register.html', context)

        # duplicate email
        if User.objects.filter(email=request.POST['email']).exists():
            context = {'message': 'متاسفانه \
                       این ایمیل قبلا استفاده شده است. \
                       در صورتی که این ایمیل شما است،\
                        از صفحه ورود گزینه فراموشی پسورد رو انتخاب کنین. \
                       ببخشید که فرم ذخیره نشده. درست می شه'} #TODO: forgot password
            #TODO: keep the form data
            return render(request, 'register.html', context)
        #if user does not exists
        if not User.objects.filter(username=request.POST['username']).exists():
                code = get_random_string(length=32)
                now = datetime.now()
                email = request.POST['email']
                password = make_password(request.POST['password'])
                username = request.POST['username']
                temporarycode = Passwordresetcodes(
                    email=email, time=now, code=code, 
                    username=username, password=password)
                temporarycode.save()
                
                context = {'message': \
                           "برای فعال کردن اکانت بستون خود \
                            روی لینک روبرو کلیک کنید\
                                  :\{}?email={}&code={}".\
                                      format(request.build_absolute_uri(\
                    '/accounts/register/'), \
                                             email, code)}
                
                #print "برای فعال کردن اکانت بستون خود روی لینک روبرو کلیک کنید :\
                #  http://bestoon.ir/accounts/register/?email={}&code={}". format(email, code)


                #message = PMMail(api_key = settings.POSTMARK_API_TOKEN,
                #                 subject = "فعال سازی اکانت بستون",
                #                 sender = "mohbde@yahoo.com",
                #                 to = email,
                #                 text_body = "برای فعال \
                # اکانت بستون خود روی لینک روبرو کلیک کنید\
                # : http://bestoon.ir/accounts/register/?code={}".\
                # format(code),
                #                 tag = "account request")
                #message.send()
                
                
                #context = {'message':\
                #            'ایمیلی حاوی لینک فعال سازی اکانت \
                #                به شما فرستاده شده، \
                #                    لطفا پس از چک کردن ایمیل، روی لینک کلیک کنید.'}
                return render(request, 'index.html', context)
        else:
            context = {'message': \
                       'متاسفانه این نام کاربری قبلا استفاده شده است. \
                        از نام کاربری دیگری استفاده کنید. \
                            ببخشید که فرم ذخیره نشده. درست می شه'}
            #TODO: forgot password
            #TODO: keep the form data
            return render(request, 'register.html', context)
    elif request.GET.has_key('code'):  # user clicked on code
        #email = request.GET['email'] (THIS WAS IN A COMMIT, MAYBE IT WILL BE BACK)
        code = request.GET['code']
        if Passwordresetcodes.objects.filter\
            (code=code).exists(): 
            #if code is in temporary db, read the data and create the user
            
            
            new_temp_user = Passwordresetcodes.objects.get(code=code)
            newuser = User.objects.create\
                (username=new_temp_user.username, \
                 password=new_temp_user.password, email=new_temp_user.email)
            this_token = get_random_string(length=48)
            token = Token.objects.create(user=newuser, token=this_token)
            #delete the temporary activation code from db
            Passwordresetcodes.objects.filter(code=code).delete()
            
            

            context = {'message':\
                        'اکانت شما ساخته شد. توکن شما\
                              {} است. آن را ذخیره کنید زیرا دیگر نمایش داده نخواهد شد.!\
                                  جدی'.format(this_token)}
            return render(request, 'index.html', context)
        else:
            context = {
                'message': 'این کد فعال سازی معتبر نیست. در صورت نیاز دوباره تلاش کنید'}
            return render(request, 'register.html', context)
    else:
        context = {'message': ''}
        return render(request, 'register.html', context)



#return username based on sent POST Token 
@csrf_exempt
def whoami(request):
    this_token = request.POST['token']  # TODO: Check if there is no `token`
    # Check if there is a user with this token; will retun 404 instead.
    this_user = get_object_or_404(User, token__token=this_token)

    return JsonResponse({
        'user': this_user.username,
    }, encoder=JSONEncoder)   #return {'user':'USERNAME'}



#return General Status of a user as Json (income,expense)
@csrf_exempt
def generalstat(request):
    # TODO: should get a valid duration (from - to), if not, use 1 month
    # TODO: is the token valid?
    print request.GET
    print request.POST
    this_token = request.POST['token']
    this_user = get_object_or_404(User, token__token=this_token)
    income = Income.objects.filter(user=this_user).aggregate(
        Count('amount'), Sum('amount'))
    expense = Expense.objects.filter(user=this_user).aggregate(
        Count('amount'), Sum('amount'))
    context = {}
    context['expense'] = expense
    context['income'] = income
    return JsonResponse(context, encoder=JSONEncoder)  #return {'income':'INCOME','expanse':'EXPENSE'}


#homepage of System
def index(request):
    context = {}
    return render(request, 'index.html', context)


#submit an income to system (api) , input : token(POST) , output : status = (ok)
@csrf_exempt
def submit_income(request):
    """ submit an income """

    # TODO; validate data. user might be fake. token might be fake, \
    # amount might be...
    # TODO: is the token valid?
    this_token = request.POST['token']
    this_user = get_object_or_404(User, token__token=this_token)
    if 'date' not in request.POST:
        date = datetime.now()
    else:
        date = request.POST['date']
    Income.objects.create(user=this_user, amount=request.POST['amount'],
                          text=request.POST['text'], date=date)

    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder) #return {'status':'ok'}


#submit an expense to system (api) , input : token(POST) , output : status = (ok)
@csrf_exempt
def submit_expense(request):
    """ submit an expense """

    # TODO; validate data. user might be fake. token might be fake, \
    # amount might be...
    # TODO: is the token valid?
    this_token = request.POST['token']
    this_user = get_object_or_404(User, token__token=this_token)
    if 'date' not in request.POST:
        date = datetime.now()
    else:
        date = request.POST['date']
    Expense.objects.create(user=this_user, amount=request.POST['amount'],
                           text=request.POST['text'], date=date)

    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder) #return {'status':'ok'}



###################################################################3
######################################################################
#############################################################



# -*- coding: utf-8 -*-

#from __future__ import unicode_literals
#import requests
#import random
#import string
#import time


#from django.contrib.auth import authenticate, login, logout
#from django.views.decorators.http import require_POST
#from postmark import PMMail

#from .utils import grecaptcha_verify, RateLimited

# Create your views here.


##############################################################
##############################################################
##############################################################
##############################################################
##############################################################


#def get_client_ip(request):
#    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#    if x_forwarded_for:
#        ip = x_forwarded_for.split(',')[0]
#    else:
#        ip = request.META.get('REMOTE_ADDR')
#    return ip


#def grecaptcha_verify(request):
#    data = request.POST
#    captcha_rs = data.get('g-recaptcha-response')
#    url = "https://www.google.com/recaptcha/api/siteverify"
#    params = {
#        'secret': settings.RECAPTCHA_SECRET_KEY,
#        'response': captcha_rs,
#        'remoteip': get_client_ip(request)
#    }
#    verify_rs = requests.get(url, params=params, verify=True)
#    verify_rs = verify_rs.json()
#    return verify_rs.get("success", False)
