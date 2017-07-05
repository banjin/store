from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import csv
import codecs
# Create your views here.
@csrf_exempt
def get_page(request):
    print "hahaha"
    print request.body
    print request.FILES
    servers_file = request.FILES.get('csv_file')
    csv_coding = 'gbk'
    dialect = csv.Sniffer().sniff(codecs.EncodedFile(servers_file, csv_coding).read(1024))
    servers_file.open()
    reader = csv.reader(codecs.EncodedFile(servers_file, csv_coding), delimiter=str(','), dialect=dialect)
    header = reader.next()
    header = [h.decode(csv_coding) for h in header]
    print header
    # print s.read(1024*1024)
    return HttpResponse("Hello, world. You're at the polls index.")

