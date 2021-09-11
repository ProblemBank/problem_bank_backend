
from problembank.serializers import DescriptiveProblem
from django.contrib import admin

from problembank.models import *
from Game.view.submitview import *
from problembank.forms import ProblemForm

admin.site.register(Event)
admin.site.register(BankAccount)
admin.site.register(DescriptiveAnswer)
# @admin.register(JudgeableSubmit)
# class JugeableSubmitAdmin(admin.ModelAdmin):

#     # fields = ['mark']
#     # readonly_fields = ['get_file']

#     list_display = ('__str__')
#     list_filter = ['status', 'problem_group']
#     form = ProblemForm

#     def save_model(self, request, obj, form, change):
#         judge(None, obj.id , obj.mark)
  
#     def get_form(self, request, obj=None, **kwargs):
#         form = super(JugeableSubmitAdmin, self).get_form(request, obj, **kwargs)
#         obj.save()
#         return form