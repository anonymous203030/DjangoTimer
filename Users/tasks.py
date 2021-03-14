from celery import shared_task
from datetime import date

from django.db.models import Sum
from Users.models import UserProfile, WorkingTimeModel
from Users.views import MonthlyWorkedTime, DailyWorkedTime


@shared_task
def GetMonthlyWorkedTime(request):
	if date.day == 1:
		MonthlyWorkedTime(request)


@shared_task
def GetDailyWorkedTime(request):
	DailyWorkedTime(request)
