# coding:utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout


@csrf_exempt
def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            print login(request, user)
            response = HttpResponse("success")
            response.set_cookie('username', user.username,
                                max_age=60 * 60 * 24 * 7 * 52)
            response.set_cookie('user_id', user.id,
                                max_age=60 * 60 * 24 * 7 * 52)
            # Redirect to a success page.
            return response
        else:
            return HttpResponseRedirect(u"未激活的用户")
    else:
        # Return an 'invalid login' error message.
        return HttpResponseRedirect(u"密码错误或者用户名错误")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(u"退出系统")
