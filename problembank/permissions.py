from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from django.utils import timezone

from problembank.models import BankAccount, Event, JudgeableSubmit, Problem, ProblemGroup
import datetime

JUST_VIEW_METHODS = ['GET']
JUST_ADD_AND_VIEW_METHODS = ['POST', 'GET']
JUST_ADD_METHODS = ['POST']
EDIT_AND_DELET_METHODS = ['POST', 'GET', 'PUT', 'DELETE', 'PATCH']
SAFE_METHODS = ['POST', 'GET', 'PUT', 'DELETE', 'PATCH']
"""
POST = ADD NEW ONE
PUT, PATCH = CHANGE
GET = READ
DELETE = DELETE
"""
class DefualtPermission(BasePermission):
    def is_get_list_request(self, request):
        return 'pk' not in request.parser_context['kwargs'].keys() and request.method in ['GET']

    def has_anonymous_permission(self, request, view):
        return False 
        
    def has_member_permission(self, request, view):
        return request.method in JUST_ADD_AND_VIEW_METHODS    
    
    def has_admin_prmission(self, request, view):
        return request.method in EDIT_AND_DELET_METHODS

    def has_permission(self, request, view):
        if request.user.is_anonymous :
            return self.has_anonymous_permission(request, view)
        elif request.user.account.is_mentor() :
            return self.has_member_permission(request, view)
        elif request.user.account.is_admin():
            return self.has_admin_prmission(request, view)
        else :
            return False

class ModelPermission(DefualtPermission):
    model = None
    def get_owner_id(self, request):
        obj = self.get_object(request)
        if obj is None:
            return None
        return obj.author.id

    def get_object(self, request):
        if 'pk' not in request.parser_context['kwargs'].keys():
            return None
        try:
            pk = request.parser_context['kwargs']['pk']
            obj = self.model.objects.get(pk=pk)
        except:
            return None
        return obj
        
    def is_my_object(self, request):
        return request.user.account.id == self.get_owner_id(request)
        
 
class TopicPermission(ModelPermission):
    def has_member_permission(self, request, view):
        return request.method in JUST_VIEW_METHODS    

class SubtopicPermission(ModelPermission):
    pass   

class SourcePermission(ModelPermission):
    pass


class ProblemPermission(ModelPermission):
    model = Problem
    def has_anonymous_permission(self, request, view):
        return False 
    
    def some_where_is_mentor(self, request):
        account = request.user.account
        problem = self.get_object(request)
        my_events = Event.objects.filter(mentors__in=[account]) | Event.objects.filter(owner=account)
        problem_groups = ProblemGroup.objects.filter(event__in=my_events, problems__in=[problem])
        return len(problem_groups) > 0
    
    def some_where_is_participant(self, request):
        account = request.user.account
        problem = self.get_object(request)
        my_events = Event.objects.filter(participants__in=[account])
        problem_groups = ProblemGroup.objects.filter(event__in=my_events, problems__in=[problem], is_visible=True)
        return len(problem_groups) > 0
    
    def is_visibale(self, request):
        obj = self.get_object(request)
        if obj is not None:
            return not obj.is_private
        else:
            return False

    def has_member_permission(self, request, view):
        return  (request.method in JUST_ADD_METHODS) or\
                (request.method in JUST_VIEW_METHODS and self.some_where_is_participant(request)) or\
                (request.method in EDIT_AND_DELET_METHODS and self.some_where_is_mentor(request)) or\
                (request.method in EDIT_AND_DELET_METHODS and self.is_my_object(request)) or\
                (request.method in JUST_VIEW_METHODS and self.is_visibale(request))
    
# class SubmitPermission(ModelPermission):
#     model = None
#     def get_object(self, request):
#         return None
#         # if  'sid' not in request.parser_context['kwargs'].keys() and\
#         #     'pk' not in request.parser_context['kwargs'].keys():
#         #     return None
#         # try:
#         #     pk = request.parser_context['kwargs']['sid']
#         #     obj = self.model.objects.get(pk=pk)
#         # except:
#         #     try:
#         #         pk = request.parser_context['kwargs']['pk']
#         #         obj = self.model.objects.get(pk=pk)
#         #     except:
#         #         return None
#         # return obj
#     def get_problem_group(self, request):
#         return None
#     def get_problem(self, request):
#         return None
#     def has_anonymous_permission(self, request, view):
#         return False 
    
#     def is_mentor(self, request):
#         account = request.user.account
#         problem_group = self.get_problem_group(request)
#         if problem_group is not None and problem_group is not None:
#             return len(problem_group.event.mentors.all().filter(id=account.id)) > 0 or\
#                     self.is_my_object(request)
#         return False

#     def is_participant(self, request):
#         account = request.user.account
#         problem_group = self.get_problem_group(request)
#         if problem_group is not None and problem_group is not None:
#             return len(problem_group.event.participants.all().filter(id=account.id)) > 0
#         return False
    
#     def is_my_object(self, request):
#         obj = self.get_object(request)
#         account = request.user.account
#         if obj is None:
#             return False
#         return len(obj.respondents.all().filter(id=account.id)) > 0
        
#     def is_poblic_problem(self, request):
#         problem = self.get_problem(request)
#         if problem is None:
#             return False
#         return problem.is_private == False

#     def has_member_permission(self, request, view):
#         return  (request.method in JUST_ADD_METHODS and self.is_participant(request)) or\
#                 (request.method in JUST_VIEW_METHODS and self.is_my_object(request)) or\
#                 (request.method in EDIT_AND_DELET_METHODS and self.is_mentor(request)) or\
#                 (request.method in JUST_ADD_METHODS and self.is_poblic_problem(request))

class JudgePermission(ModelPermission):
    model = JudgeableSubmit

    def is_my_object(self, request):
        obj = self.get_object(request)
        if obj is None:
            return False
        
        return obj.respondents.all().filter(id=request.user.account.id) > 0
    
    def get_problem_group(self, request):
        obj = self.get_object(request)
        if obj is None or obj.problem_group is None:
            return False
        return obj.problem_group
    
    def has_anonymous_permission(self, request, view):
        return False 
    
    def is_mentor(self, request):
        account = request.user.account
        problem_group = self.get_problem_group(request)
        if problem_group is not None and problem_group is not None:
            return len(problem_group.event.mentors.all().filter(id=account.id)) > 0 or\
                    (problem_group.event.owner.id == account.id)
        return False

    def has_member_permission(self, request, view):
        return request.method in JUST_ADD_METHODS and self.is_mentor(request)
                
class SubmitAnswerPermission(ModelPermission):
    def get_problem_group(self, request):
        if 'gid' not in request.parser_context['kwargs'].keys():
            return None
        try:
            pk = request.parser_context['kwargs']['gid']
            obj = ProblemGroup.objects.get(pk=pk)
        except:
            return None
        return obj

    def has_anonymous_permission(self, request, view):
        return False 
    
    def is_participant(self, request):
        account = request.user.account
        problem_group = self.get_problem_group(request)
        if problem_group is not None and problem_group is not None:
            return len(problem_group.event.participants.all().filter(id=account.id)) > 0
        return False
    
    def has_member_permission(self, request, view):
        return request.method in JUST_ADD_METHODS and self.is_participant(request)


class ProblemGroupPermission(ModelPermission):
    model = ProblemGroup
    def get_owner_id(self, request):
        event = self.get_event(request)
        if event is not None:
            return event.owner.id

    def get_event(self, request):
        problem_group = self.get_object(request)
        if problem_group is not None:
            return problem_group.event
        else:
            try:
                return Event.objects.get(pk=request.data['event'])
            except:
                None

    def is_mentor(self, request):
        account = request.user.account
        event = self.get_event(request)
        if event is not None:
            return len(event.mentors.all().filter(id=account.id)) > 0 or\
                    self.is_my_object(request)
        return False

    def is_participant(self, request):
        account = request.user.account
        event = self.get_event(request)
        if event is not None:
            return len(event.participants.all().filter(id=account.id)) > 0
        return False
    
    def has_member_permission(self, request, view):
        return (request.method in JUST_VIEW_METHODS and self.is_participant(request)) or\
                (request.method in EDIT_AND_DELET_METHODS and self.is_mentor(request))

class AddProblemToGroupPermission(ProblemGroupPermission):
    def get_object(self, request):
        if 'gid' not in request.parser_context['kwargs'].keys():
            return None
        try:
            pk = request.parser_context['kwargs']['gid']
            obj = self.model.objects.get(pk=pk)
        except:
            return None
        return obj
    
class EventPermission(ModelPermission):
    model = Event
    def get_owner_id(self, request):
        obj = self.get_object(request)
        if obj is None:
            return None
        return obj.owner.id

    def is_member(self, request):
        event = self.get_object(request)
        account = request.user.account
        if event is not None:
            return len(event.mentors.all().filter(id=account.id)) > 0 or\
                    len(event.participants.all().filter(id=account.id)) > 0 or\
                    self.is_my_object(request)
        return False

    def has_member_permission(self, request, view):
        return request.method in JUST_ADD_METHODS or\
                (request.method in JUST_VIEW_METHODS and self.is_member(request)) or\
                (request.method in EDIT_AND_DELET_METHODS and self.is_my_object(request))