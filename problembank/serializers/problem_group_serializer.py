from rest_framework import serializers
from problembank.models import ProblemGroup

class ProblemGroupSerializerWithoutProblems(serializers.ModelSerializer):

    class Meta:
        model = ProblemGroup
        exclude = ('problems',)