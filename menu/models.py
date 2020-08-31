from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime
# Create your models here.

class UserInfo(models.Model):
	# index값을 넣지 않으려면 bulk_create시 row[1]부터 받야야 한다
	uid = models.CharField(max_length = 64)
	accountId = models.CharField(max_length = 57)
	puuid = models.CharField(max_length = 79)
	name = models.CharField(max_length = 30)
	profileIconId = models.CharField(max_length = 30)
	revisionDate = models.IntegerField()   #나중에 DateTimeField로 변경 필요(유닉스 시간)
	summonerLevel = models.IntegerField()

	# def convert_unixtime(date_time):
 #    """Convert datetime to unixtime"""
 #    import datetime
 #    unixtime = datetime.datetime.strptime(date_time,
 #                               '%Y-%m-%d %H:%M:%S,%f').timestamp()
 #    unixtime_mili = unixtime * 1000
 #    return unixtime_mili
 #    datetime.datetime.fromtimestamp(1597391105)

	def __str__(self): #이 클래스의 object를 표현할 때 어떻게 할지
		return self.name #object를 출력하면 name이 보입니다.

class MatchList(models.Model):
	# index값을 넣지 않으려면 bulk_create시 row[1]부터 받야야 한다
	platformId = models.CharField(max_length = 10)
	gameId = models.IntegerField(default=0)
	champion = models.IntegerField(default=0)
	queue =models.IntegerField(default=0)
	seaon = models.IntegerField(default=1)
	timestamp = models.IntegerField(default=0)   #나중에 DateTimeField로 변경 필요(유닉스 시간)
	role = models.CharField(max_length = 15)
	lane = models.CharField(max_length = 10)
	accountId = models.CharField(max_length = 57)