from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from datetime import date
from rest_framework import serializers
from django.db.models.aggregates import Sum


class UserManage(BaseUserManager):
	def create_user(self, username, email, password = None):
		if username is None:
			raise TypeError('users should have an username')
		if email is None:
			raise TypeError('users should have an email')

		user = self.model(username = username, email = self.normalize_email(email))
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, username, email, password):
		if password is None:
			raise TypeError('Password should not to be none.')

		user = self.create_user(username, email, password)
		user.is_superuser = True
		user.is_staff = True
		user.save()
		return user


class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(max_length = 50, unique = True, db_index = True)
	email = models.EmailField(max_length = 50, unique = True, db_index = True)
	is_superuser = models.BooleanField(default = False)
	is_staff = models.BooleanField(default = False)
	created_at = models.DateField(auto_now_add = True)
	updated_at = models.DateField(auto_now = True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = UserManage()

	def __str__(self):
		return self.email


class UserProfile(models.Model):
	GENDER = (
			('M', 'Male'),
			('F', 'Female')
	)
	image = models.FileField(upload_to = 'profile_img/', blank = True, )
	first_name = models.CharField(max_length = 100)
	last_name = models.CharField(max_length = 100)
	about = models.TextField()
	birthday = models.DateField(auto_now_add = False)
	gender = models.CharField(choices = GENDER, max_length = 100, )
	owner = models.OneToOneField(User, on_delete = models.CASCADE)
	salary_for_hour = models.IntegerField(default = 0)

	# month_working_time = models.IntegerField()
	def __str__(self):
		return f'{User.username}:{self.first_name} {self.last_name}'


class WorkingTimeModel(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
	start_time = models.TimeField()
	# break_time = models.FloatField(default=0)
	end_time = models.TimeField()
	created_date = models.DateTimeField(auto_now_add = True)
	updated_date = models.DateTimeField(auto_now = True)
	daily_working_time = models.SmallIntegerField()

	def __str__(self):
		return f"{self.end_time}"

	def save(self, *args, **kwargs):
		self.daily_working_time = (self.end_time.hour - self.start_time.hour) * 60 + \
		                          self.end_time.minute - self.start_time.minute
		if self.daily_working_time <= 0:
			raise serializers.ValidationError('NEGATIVE Number')
		super(WorkingTimeModel, self).save(*args, **kwargs)


class BreakTime(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
	start_time = models.TimeField()
	end_time = models.TimeField()
	created_date = models.DateTimeField(auto_now_add = True)
	updated_date = models.DateTimeField(auto_now = True)
	break_time = models.FloatField(default = 0)

	def __str__(self):
		return f"Owner: {self.owner} | Break Time: {(self.end_time.hour - self.start_time.hour) * 60 + self.end_time.minute - self.start_time.minute}| Created At {self.created_date} "

	def save(self, *args, **kwargs):
		self.break_time = (self.end_time.hour - self.start_time.hour) * 60 + \
		                  self.end_time.minute - self.start_time.minute
		if self.break_time < 0:
			raise serializers.ValidationError('NEGATIVE Number')
		super(BreakTime, self).save(*args, **kwargs)


class GetDailyResult(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
	daily_worked_time = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return f'Daily Worked Time {self.daily_worked_time} | Created At {self.created_at}'


class GetMonthlyResult(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
	salary = models.IntegerField(blank = True, null = True)
	monthly_worked_time = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add = True)
