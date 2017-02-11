import requests
import json
from django.http import HttpResponse
from main.models import data , Users 
from django.shortcuts import redirect , render



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
	





def graph(request):
	uid = request.GET.get('uid')
	disease = request.GET.get('disease')
	v = Users.objects.get(uid = uid)
	pk = v.pk

	u = data.objects.filter(typeof = disease)
	c = []
	for i in u:
		date = i.date
		duration = i.duration
		severity  = i.severity

		elem = json.dumps({"date":date,"duration" :duration, "severity" :severity})
		c.append(elem)



	response_obj = json.dumps(c)
	return HttpResponse(response_obj)


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