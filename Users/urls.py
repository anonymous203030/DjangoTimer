from django.urls import path

from .views import *

p = 'profile/'
urlpatterns = [
		# USER
		path(f'register/', RegisterViewSet.as_view(), name = 'user_register'),
		path(f'user/login/', LoginAPiViewSet.as_view(), name = 'user_login'),
		path(f'user/list/', UsersListViewSet.as_view(), name = 'user_list'),
		# PROFILE urls
		path(f'{p}create/', UserProfileCreateViewSet.as_view(), name = 'create_profile'),
		path(f'{p}list/', UserProfileListViewSet.as_view(), name = 'list_profile'),
		# path(f'{p}detail/<int:pk>/', UserProfileDetailViewSet.as_view(), name='change_profile'),
		# Working Time urls
		path(f'create/', WorkingTimeCreateViewSet.as_view(), name = 'create_time'),
		# path(f'detail/', WorkingTimeDetailViewSet.as_view(), name='detail_time'),
		path(f'list/', WorkingTimeListViewSet.as_view(), name = 'list_time'),
		# Break Time urls
		path(f'break/create/', AddBreakTimeCreate.as_view(), name = 'break_create'),
		# path(f'break/detail/<int:pk>/', AddBreakTimeDetail.as_view(), name='break_detail'),
		path(f'break/list/', AddBreakTimeList.as_view(), name = 'break_list'),
		path(f'amount/daily/', DailyWorkedTime, name = 'daily_amount'),
		path(f'amount/monthly/', MonthlyWorkedTime, name = 'monthly_amount'),
]
