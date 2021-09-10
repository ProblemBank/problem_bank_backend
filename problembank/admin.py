
from problembank.serializers import DescriptiveProblem
from django.contrib import admin

from problembank.models import *
from Game.view.submitview import *
from problembank.forms import QuestionForm
class AnswerInline(admin.TabularInline):  # StackedInline
    model = DescriptiveAnswer
    extra = 1

@admin.register(JudgeableSubmit)
class JugeableSubmitAdmin(admin.ModelAdmin):

    fields = ['text_tmp1', 'text_tmp2', 'get_file', 'mark']
    readonly_fields = ['get_file']

    list_display = ('__str__', 'status')
    list_filter = ['status', 'problem_group']
    # inlines = (AnswerInline,)
    form = QuestionForm
    # inlines = (HardnessInline,)

    # all defualt saved for each users
    def save_model(self, request, obj, form, change):
        judge(None, obj.id , obj.mark)
  
    def get_form(self, request, obj=None, **kwargs):
        form = super(JugeableSubmitAdmin, self).get_form(request, obj, **kwargs)
        obj.text_tmp1 = obj.get_problem()
        obj.text_tmp2 = obj.get_answer()
        obj.save()
        return form