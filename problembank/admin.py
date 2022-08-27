
from problembank.serializers import DescriptiveProblem
from django.contrib import admin

from problembank.models import *
from problembank.forms import ProblemForm
from problembank.utils import generate_password

admin.site.register(ProblemGroup)
admin.site.register(BankAccount)
admin.site.register(ShortAnswerProblem)
admin.site.register(DescriptiveProblem)
admin.site.register(Topic)
admin.site.register(ShortAnswer)
admin.site.register(JudgeableSubmit)



@admin.register(AutoCheckSubmit)
class AutoCheckSubmitAdmin(admin.ModelAdmin):
    list_filter = ['problem', 'respondents']


@admin.register(Subtopic)
class SubTopicAdmin(admin.ModelAdmin):
    list_filter = ['topic']


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
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    # all defualt saved for each users
    def save_model(self, request, obj, form, change):
        if obj.mentor_password == 'gen':
            obj.mentor_password = generate_password(8)
        if obj.participant_password == 'gen':
            obj.participant_password = generate_password(8)

        obj.save()
