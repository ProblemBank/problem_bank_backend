
from problembank.serializers import DescriptiveProblem
from django.contrib import admin

from problembank.models import *
from Game.view.submitview import *
class AnswerInline(admin.TabularInline):  # StackedInline
    model = DescriptiveAnswer
    extra = 1

@admin.register(JudgeableSubmit)
class JugeableSubmitAdmin(admin.ModelAdmin):

    fields = ['get_problem', 'get_answer', 'get_file', 'mark']
    readonly_fields = ['get_problem', 'get_answer', 'get_file']

    list_display = ('__str__', 'status')
    list_filter = ['status', 'problem_group']
    # inlines = (AnswerInline,)
    # form = QuestionForm
    # inlines = (HardnessInline,)

    # all defualt saved for each users
    def save_model(self, request, obj, form, change):
        judge(None, obj.id , obj.mark)
        # obj.save()
    #     # print(obj.text.encode())
    #     if change:
    #         pass
    #         # obj.question_maker = request.user.account
    #         # obj.publish_date = timezone.localtime()

    #     #if obj.question_maker.role == 'a': request.user.account.role
    #     #    obj.verification_status = 'w'

    #     #obj.change_date = timezone.localtime()
    #     obj.save()


