from django.shortcuts import render
from .models import UserInfo, MatchList
# Create your views here.

def menu_list(request):
	infos = UserInfo.objects.all()
	context = {'infos' : infos}
	return render(request, 'menu/menu_list.html', context)

def info_list(request):
	query = request.GET['query']
	if query:
		infos = UserInfo.objects.filter(name = query)
		#accountId = UserInfo.objects.get(name = query)
		for info in infos:
			accountId = info.accountId
		matches = MatchList.objects.filter(accountId = accountId)
		#matches = MatchList.objects.all()
		context = {'infos' : infos, 'matches' : matches }
		#context = {'infos' : infos}
	return render(request, 'menu/info_list.html', context)


def object_list(request):
	infos = UserInfo.objects.all()
	context = {'infos' : infos}
	return render(request, 'menu/object_list.html', context)

def champion_list(request):
	infos = UserInfo.objects.all()
	context = {'infos' : infos}
	return render(request, 'menu/champion_list.html', context)