from django.contrib import admin

from .models import User, UserProfile, WorkingTimeModel, BreakTime, GetMonthlyResult, GetDailyResult
from .views import DailyWorkedTime, MonthlyWorkedTime


# Admin Settings


class UsersAdmin(admin.ModelAdmin):
	list_display = ('username', 'email', 'is_staff', 'created_at', 'updated_at',)
	list_filter = ('is_staff', 'created_at', 'updated_at',)
	ordering = ('created_at',)
	fieldsets = (
			(None, {'fields': ('email', 'username', 'password')}),
			('Permissions', {'fields': ('is_superuser', 'is_staff')}),
	)

	add_fieldsets = (
			(None, {
					'classes': ('wide',),
					'fields': ('email', 'password1', 'password2'),
			}),
	)
	search_fields = ('username', 'email',)


admin.site.register(User, UsersAdmin)


class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'birthday', 'gender', 'owner', 'image', 'salary_for_hour',)
	list_filter = ('birthday', 'gender', 'owner',)
	ordering = ('first_name',)
	search_fields = ('first_name', 'last_name',)

	fieldsets = [
			("Worker", {'fields': ['owner'],
			            'classes': ['collapse']}),
			('About worker', {'fields': (('first_name', 'last_name'), ('birthday', 'gender'), 'image', 'about'),
			                  'classes': ['collapse']}),
			('Salary', {'fields': ['salary', 'salary_for_hour'],
			            'classes': ['collapse']})
	]


admin.site.register(UserProfile, UserProfileAdmin)


class WorkingTimeAdmin(admin.ModelAdmin):
	# title = ['owner', 'start_time', 'end_time', 'break_time', 'created_date', 'updated_date']
	list_display = ('owner', 'start_time', 'end_time', 'created_date', 'updated_date',)
	list_filter = ('owner', 'created_date',)
	ordering = ('created_date',)
	search_fields = ('owner__first_name', 'owner__last_name', 'created_date',)
	readonly_fields = ['daily_working_time']


admin.site.register(WorkingTimeModel, WorkingTimeAdmin)


class BreakTimeAdmin(admin.ModelAdmin):
	list_display = ('owner', 'start_time', 'end_time', 'created_date', 'updated_date', 'break_time', )
	list_filter = ('owner', 'created_date',)
	ordering = ('created_date',)
	search_fields = ('owner__first_name', 'owner__last_name', 'created_date',)
	readonly_fields = ['break_time']


admin.site.register(BreakTime, BreakTimeAdmin)


class MonthlyResultAdmin(admin.ModelAdmin):
	list_display = ['owner', 'created_at', 'monthly_worked_time', 'salary']
	list_filter = ['created_at']
	readonly_fields = ['monthly_worked_time', 'salary']

	def save_model(self, request, obj, form, change):
		MonthlyWorkedTime(request)


admin.site.register(GetMonthlyResult, MonthlyResultAdmin)


class DailyResultAdmin(admin.ModelAdmin):
	list_display = ['owner', 'created_at', 'daily_worked_time']
	list_filter = ['created_at']
	readonly_fields = ['daily_worked_time']

	def save_model(self, request, obj, form, change):
		DailyWorkedTime(request)


admin.site.register(GetDailyResult, DailyResultAdmin)
