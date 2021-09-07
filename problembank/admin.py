
from problembank.views.problemcategoryview import ProblemCategoryView
from problembank.serializers import DescriptiveProblem
from django.contrib import admin

from problembank.models import *

admin.site.register(Problem)
admin.site.register(ShortAnswerProblem)
admin.site.register(DescriptiveProblem)
admin.site.register(BankAccount)
admin.site.register(ShortAnswer)
admin.site.register(ProblemCategory)
admin.site.register(Topic)