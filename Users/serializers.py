from datetime import datetime, date

from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from src import settings
from .models import User, UserProfile, WorkingTimeModel, BreakTime, GetDailyResult, GetMonthlyResult
from django.contrib import auth


class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(max_length = 50, min_length = 8)

	class Meta:
		model = User
		fields = ('id', 'email', 'username', 'password',)
		ordering = ['-id']

	def validate(self, attrs):
		# email = attrs.get('email', '')
		username = attrs.get('username', '').strip()

		if not username.isalnum():
			raise serializers.ValidationError('The Username Should'
			                                  'Only Contain Alpha Characters')
		return attrs

	def create(self, validated_data):
		return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(max_length = 50, min_length = 6)
	password = serializers.CharField(max_length = 50, min_length = 3, write_only = True)
	username = serializers.CharField(read_only = True)

	class Meta:
		model = User
		fields = ('id', 'email', 'password', 'username',)
		ordering = ['-id']

	def validate(self, attrs):
		email = attrs.get('email', '')
		password = attrs.get('password', '')

		user = auth.authenticate(email = email, password = password)
		if not user:
			raise AuthenticationFailed('Invalid credentials,try again')
		if not user.is_active:
			raise AuthenticationFailed('Account Disabled')
		return {
				'email': user.email,
				'username': user.username,
				# 'password':user.password
		}


class UserProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserProfile
		fields = '__all__'
		# ('id', 'image', 'first_name', 'last_name', 'about', 'birthday', 'gender', 'owner', 'salary', )
		ordering = ['-id']

	def get_salary(self, instance):
		pass


class UserSerializer(serializers.ModelSerializer):
	# profile = UserProfileSerializer()

	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'is_staff', 'created_at', 'updated_at',)
		ordering = ['-id']


class WorkingTimeSerializer(serializers.ModelSerializer):
	class Meta:
		model = WorkingTimeModel
		fields = '__all__'
		read_only_fields = ['owner', 'daily_working_time']
		ordering = ['-id']


# exclude = ('salary', )


class AddBreakTimeSerializer(serializers.ModelSerializer):
	# start_time = serializers.TimeField(input_formats = settings.TIME_FORMAT)
	# end_time = serializers.TimeField(input_formats = settings.TIME_FORMAT)

	class Meta:
		model = BreakTime
		fields = '__all__'
		# read_only_fields = ['owner']
		ordering = ['-id']
		read_only_fields = ['owner', 'break_time']

# readonly_fields = ['owner', 'break_time']


# GENERATE
class DailyWorkedTimeSerializer(serializers.ModelSerializer):
	class Meta:
		model = GetDailyResult
		fields = '__all__'


class MonthlyWorkedTimeSerializer(serializers.ModelSerializer):
	class Meta:
		model = GetMonthlyResult
		fields = '__all__'
		# read_only_fields = '__all__'
