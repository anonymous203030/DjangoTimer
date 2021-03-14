from datetime import datetime, timedelta
from datetime import date
from django.http import HttpResponse, Http404
from rest_framework import generics, status, filters
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render, redirect

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .filters import IsOwnerFilter
from .models import User, UserProfile, WorkingTimeModel, BreakTime, GetDailyResult, GetMonthlyResult
from .permissions import IsOwner
from .serializers import (LoginSerializer, UserSerializer, UserProfileSerializer, WorkingTimeSerializer,
                          AddBreakTimeSerializer)
from .serializers import RegisterSerializer
from django.contrib.auth.views import auth_logout
from rest_framework.decorators import api_view


# USERS ViewSets

class RegisterViewSet(generics.GenericAPIView):
	serializer_class = RegisterSerializer

	def post(self, request):
		user = request.data
		serializer = self.serializer_class(data = user)
		serializer.is_valid(raise_exception = True)
		serializer.save()

		user_data = serializer.data

		return Response(user_data, status = status.HTTP_201_CREATED)


class LoginAPiViewSet(generics.GenericAPIView):
	serializer_class = LoginSerializer

	def post(self, request):
		serializer = self.serializer_class(data = request.data)
		serializer.is_valid(raise_exception = True)
		return Response(serializer.data, status = status.HTTP_200_OK)

	def perform_create(self, serializer):
		queryset = LoginSerializer.objects.filter(user = self.request.user)
		if queryset.exists():
			raise ValidationError('You have already signed up')
		serializer.save()


class UsersListViewSet(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [IsAdminUser]
	pagination_class = PageNumberPagination
	filter_backends = [filters.SearchFilter,
	                   filters.OrderingFilter]
	search_fields = ['username', 'email']
	ordering_fields = ['created_at', 'updated_at']
	filterset_fields = ['created_at', 'updated_at']


# USER PROFILE ViewSets
class UserProfileListViewSet(generics.ListAPIView):
	queryset = UserProfile.objects.all()
	serializer_class = UserProfileSerializer
	permission_classes = [IsAdminUser]
	pagination_class = PageNumberPagination
	filter_backends = [filters.SearchFilter,
	                   filters.OrderingFilter]
	search_filters = ['first_name', 'last_name', 'owner']
	ordering_fields = ['owner__created_at', 'owner__updated_at']
	filterset_fields = ['birthday', 'gender']


class UserProfileCreateViewSet(generics.CreateAPIView):
	queryset = UserProfile.objects.all()
	serializer_class = UserProfileSerializer
	permission_classes = [IsOwner]


# class UserProfileDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
# 	queryset = UserProfile.objects.all()
# 	serializer_class = UserProfileSerializer
# 	permission_classes = [IsOwner]


# Working Time ViewSets
class WorkingTimeCreateViewSet(generics.CreateAPIView):
	queryset = WorkingTimeModel.objects.all()
	serializer_class = WorkingTimeSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.validated_data['owner'] = self.request.user
		serializer.save()


# class WorkingTimeDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
# 	queryset = WorkingTimeModel.objects.all()
# 	serializer_class = WorkingTimeSerializer
# 	permission_classes = [IsAdminUser]


class WorkingTimeListViewSet(generics.ListAPIView):
	queryset = WorkingTimeModel.objects.all()
	serializer_class = WorkingTimeSerializer
	permission_classes = [IsOwner]
	pagination_class = PageNumberPagination
	filter_backends = [filters.SearchFilter,
	                   filters.OrderingFilter, IsOwnerFilter]
	ordering_fields = ['created_date', 'updated_date', 'daily_working_time']


# Break Time ViewSet
class AddBreakTimeList(generics.ListAPIView):
	queryset = BreakTime.objects.all()
	serializer_class = AddBreakTimeSerializer
	permission_classes = [IsOwner]
	pagination_class = PageNumberPagination
	filter_backends = [filters.SearchFilter,
	                   filters.OrderingFilter, IsOwnerFilter]
	ordering_fields = ['created_date']


class AddBreakTimeCreate(generics.CreateAPIView):
	queryset = BreakTime.objects.all()
	serializer_class = AddBreakTimeSerializer
	permission_classes = [IsOwner]
	pagination_class = PageNumberPagination
	filter_backends = [filters.SearchFilter,
	                   filters.OrderingFilter, IsOwnerFilter]
	ordering_fields = ['created_date']

	def perform_create(self, serializer):
		serializer.validated_data['owner'] = self.request.user
		serializer.save()


@api_view(['GET'])
def DailyWorkedTime(request):
	# Getting worked values 'start_time' 'end_time' only for today() and for requested user
	w_start_time_list = [time['start_time'].strftime('%H:%M').split(':') for time in
	                     WorkingTimeModel.objects.filter(created_date__date = date.today(),
	                                                     owner = request.user).values('start_time',
	                                                                                  'end_time')]
	w_end_time_list = [time['end_time'].strftime('%H:%M').split(':') for time in
	                   WorkingTimeModel.objects.filter(created_date__date = date.today(),
	                                                   owner = request.user).values('start_time',
	                                                                                'end_time')]
	# Getting break time values 'start_time' 'end_time' only for today() and for requested user
	b_start_time_list = [time['start_time'].strftime('%H:%M').split(':') for time in
	                     BreakTime.objects.filter(created_date__date = date.today(), owner = request.user).values(
			                     'start_time',
			                     'end_time')]
	b_end_time_list = [time['end_time'].strftime('%H:%M').split(':') for time in
	                   BreakTime.objects.filter(created_date__date = date.today(), owner = request.user).values(
			                   'start_time',
			                   'end_time')]

	# Convert from break 'start_time' 'end_time' nested lists format
	# w_start_time_list = [time['start_time'].strptime('%H:%M').split(':') for time in daily_worked_time_list]
	# w_end_time_list = [time['end_time'].strptime('%H:%M').split(':') for time in daily_worked_time_list]
	w_time = sum(
			[(int(end[0]) - int(start[0])) * 60 + (int(end[1]) - int(start[1])) for start in w_start_time_list for end
			 in w_end_time_list])
	b_time = sum(
			[(int(end[0]) - int(start[0])) * 60 + (int(end[1]) - int(start[1])) for start in b_start_time_list for end
			 in b_end_time_list])
	Daily = GetDailyResult(owner = request.user, daily_worked_time = w_time - b_time, created_at = datetime.today())
	Daily.save()

	return Response({'Saved Successfully: Today User Worked': f'{w_time - b_time} minutes.'})


@api_view(['GET'])
def MonthlyWorkedTime(request):
	last_month = datetime.today() - timedelta(days = 30)

	m_start_time_list = [time['start_time'].strftime('%H:%M').split(':') for time in
	                     WorkingTimeModel.objects.filter(created_date__gte = last_month,
	                                                     owner = request.user).values('start_time',
	                                                                                  'end_time')]
	m_end_time_list = [time['end_time'].strftime('%H:%M').split(':') for time in
	                   WorkingTimeModel.objects.filter(created_date__gte = last_month,
	                                                   owner = request.user).values('start_time',
	                                                                                'end_time')]
	# Getting break time values 'start_time' 'end_time' only for today() and for requested user
	b_start_time_list = [time['start_time'].strftime('%H:%M').split(':') for time in
	                     BreakTime.objects.filter(created_date__gte = last_month, owner = request.user).values(
			                     'start_time',
			                     'end_time')]
	b_end_time_list = [time['end_time'].strftime('%H:%M').split(':') for time in
	                   BreakTime.objects.filter(created_date__gte = last_month, owner = request.user).values(
			                   'start_time',
			                   'end_time')]

	# Convert from break 'start_time' 'end_time' nested lists format
	# w_start_time_list = [time['start_time'].strptime('%H:%M').split(':') for time in daily_worked_time_list]
	# w_end_time_list = [time['end_time'].strptime('%H:%M').split(':') for time in daily_worked_time_list]
	m_time = sum(
			[(int(end[0]) - int(start[0])) * 60 + (int(end[1]) - int(start[1])) for start in m_start_time_list for end
			 in m_end_time_list])
	b_time = sum(
			[(int(end[0]) - int(start[0])) * 60 + (int(end[1]) - int(start[1])) for start in b_start_time_list for end
			 in b_end_time_list])

	Daily = GetMonthlyResult(owner = request.user, monthly_worked_time = m_time - b_time, created_at = datetime.today())
	Daily.save()
	return Response({'Saved Successfully: Monthly User Worked': f'{m_time - b_time} minutes.'})


# SIMPLE HTML-CSS MAIN PAGE

def login(request):
	if request.method == 'POST': return HttpResponse(":)")
	return render(request, 'login.html')


def main(request):
	return render(request, 'main.html')


def logout(request):
	if request.method == 'POST': return Http404('Something Went Wrong')
	auth_logout(request)
	return redirect('login')
