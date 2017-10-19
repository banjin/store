import threading
from django.conf.urls import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from dwebsocket.decorators import accept_websocket
from django.http import HttpResponse
import time
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


def base_view(request):
    return render_to_response('index.html', {

    })


clients = []


@accept_websocket
def echo(request):
    if request.is_websocket:
        lock = threading.RLock()
        try:
            lock.acquire()
            clients.append(request.websocket)
            for message in request.websocket:
                if not message:
                    break
                for client in clients:
                    client.send(message)
                    print "2222222"

        finally:
            clients.remove(request.websocket)
            lock.release()


def modify_message(message):
    return message.lower()


@accept_websocket
def lower_case(request):
    if not request.is_websocket():
        print "xxxxxxxx"
        print "request.......", request
        message = request.GET['message']
        print "ccccc", message
        message = modify_message(message)
        return HttpResponse(message)
    else:
        for message in request.websocket:
            print "dddd", message
            message = modify_message(message)
            i = 0
            while 1:
                i += 1
                time.sleep(1)
                request.websocket.send(message)

