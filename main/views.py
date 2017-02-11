import requests
import json
from django.http import HttpResponse
from main.models import data , Users 
from django.shortcuts import redirect , render
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Image



def index(request):
    uid = request.GET.get('uid')
    typeof = request.GET.get('typeof')
    date = request.GET.get('date')
    medicine = request.GET.get('medicine')
    duration = request.GET.get('duration')
    severity = request.GET.get('severity')

    v = Users.objects.get_or_create(uid = uid)[0]


    u = v.data_set.create()
    #u.idm = v
    u.typeof = typeof 
    u.date = date
    u.medicine = medicine 
    u.duration = duration 
    u.severity = severity 
    u.save()

    return HttpResponse("saved")


# def return_c(request):



def doc(request):

    uid = request.GET.get('uid')
    review = request.GET.get('review')
    v = Users.objects.get(uid = uid)


    u = v.data_set.get_or_create()[0]
    #u.idm = v
    u.review = review 
    u.save()
    return HttpResponse("saved")

def govt(request):
    uid = request.GET.get('uid')
    v = Users.objects.get(uid = uid)
    pk = v.pk

    u = data.objects.filter(uid = pk)
    c = []
    for i in u:
        typeof = i.typeof
        date = i.date
        medicine = i.medicine
        duration = i.duration
        severity  = i.severity
        review = i.review

        elem = {"typeof": typeof, "date":date , "medicine" :medicine , "duration" :duration, "severity" :severity, "review" :review}
        c.append(elem)



    response_obj = json.dumps(c ,indent = 4)
    return HttpResponse(response_obj , content_type = "application/json" )  

    # u.review = q['review'] 


# Create your views here.



def info(request):
    uid = request.GET.get('uid')
    v = Users.objects.get(uid = uid)
    pk = v.pk

    u = data.objects.filter(uid = pk)
    c = []
    for i in u:
        typeof = i.typeof
        date = i.date
        medicine = i.medicine
        duration = i.duration
        severity  = i.severity

        elem = {"typeof": typeof, "date":date , "medicine" :medicine , "duration" :duration, "severity" :severity}
        c.append(elem)



    response_obj = json.dumps(c , )
    return HttpResponse(response_obj)   
def category(request):
    uid = request.GET.get('uid')
    a = []
    v = Users.objects.get(uid  = uid )
    pk = v.pk

    u = data.objects.values('typeof')
    print u 

    for i in u :
        a.append(i.values()[0])

    print a
    t = list(set(a))

    response_obj = json.dumps(t)
    return HttpResponse(response_obj)
    





def graph():
    uid = request.GET.get('uid')
    disease = request.GET.get('disease')
    v = Users.objects.get(uid = uid)
    pk = v.pk

    u = data.objects.filter(typeof = disease)
    c = []
    for i in u:
        date = i.date
        # duration = i.duration
        severity  = i.severity

        elem = {date:severity}
        c.append(elem)


    # response['Content-Disposition'] = 'attachment; filename="mycv.pdf"'
    # Create the PDF object, using the response object as its "file."
#     p = canvas.Canvas(response)
# # 
#     p.setStrokeColor(colors.red)    
#     p.line(0,745,500,745)
#     p.line(0,745,0,700)

#     p.setStrokeColor(colors.black)

#     for i in c:
#       p.point(i.key,i.value)

#   response_obj = json.dumps(c)
    return c


def chart(request):
    uid = request.GET.get('uid')
    disease = request.GET.get('disease')
    v = Users.objects.get(uid = uid)
    pk = v.pk
    data1 = []

    u = data.objects.filter(uid = pk)
    x = u.filter(typeof = disease)
    severity1 = []
    for i in u:
        typeof = i.typeof
        date = i.date
        data1.append(date)

        # duration = i.duration
        severity  = i.severity
        severity1.append(severity)

    main = []
    main.append(severity1)
    main.append(data1)
    print severity1





    # return HttpResponse(main)
    return render(request, 'main/chart.html', {'severity1': json.dumps(severity1)})


def linechart(request):

#instantiate a drawing object
    import mycharts
    d = mycharts.MyLineChartDrawing()

    #extract the request params of interest.
    #I suggest having a default for everything.
    

    d.height = 300
    d.chart.height = 300
    

    d.width = 300
    d.chart.width = 300
   
    d.title._text = request.session.get('Some custom title')
    
    

    d.XLabel._text = request.session.get('X Axis Labell')
    d.YLabel._text = request.session.get('Y Axis Label')

    # uid = request.GET.get('uid')
    # disease = request.GET.get('disease')
    # v = Users.objects.get(uid = uid)
    # pk = v.pk

    # u = data.objects.filter(typeof = disease)
    # c = []
    # f = []
    # for i in u:
    #     date = i.date
    #     duration = i.duration
    #     severity  = i.severity

    #     elem = {date:severity}
    #     c.append((elem))

    # # print c    


    # for j in c:
    #     # print l.type()
    #     # print j.keys() 
    #     elemm  = (j.keys()[0],j.values()[0])
    #     f.append(elemm)

    # print f 

    d.chart.data = [((1,1), (2,2), (2.5,1), (3,3), (4,5)),((1,2), (2,3), (2.5,2), (3.5,5), (4,6))]
   

    
    labels =  ["Label One","Label Two"]
    if labels:
        # set colors in the legend
        d.Legend.colorNamePairs = []
        for cnt,label in enumerate(labels):
                d.Legend.colorNamePairs.append((d.chart.lines[cnt].strokeColor,label))


    #get a GIF (or PNG, JPG, or whatever)
    binaryStuff = d.asString('gif')
    return HttpResponse(binaryStuff, 'image/gif')