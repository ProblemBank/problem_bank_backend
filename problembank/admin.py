
from problembank.serializers import BaseProblemSerializer
from django.contrib import admin

from problembank.models import *

admin.site.register(Problem)
admin.site.register(BaseProblem)
admin.site.register(ShortAnswerProblem)
admin.site.register(BankAccount)
admin.site.register(ShortAnswer)






