from random import choice

from django.core.files import File
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from Account.models import User
from Game.models import Subject, ProblemAnswer, CometProblemAnswer, Player, Problem, CometProblem, Game, \
    Transaction, Hint
from Game.serializers import SingleProblemSerializer, SubjectSerializer, MultipleProblemSerializer, \
    ProblemDetailedSerializer, PlayerSingleProblemDetailedSerializer, PlayerSerializer, HintSerializer, \
    PlayerSingleProblemCorrectionSerializer, HintAnsweringSerializer


class HintView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = HintSerializer
    queryset = Hint.objects.all()

    def get(self, request, game_id, problem_id):
        user = request.user
        player = Player.objects.get(user=user, game__id=game_id)
        hints = Hint.objects.filter(multiple_problem__id=problem_id, player=player)
        hints_serializer = HintSerializer(data=hints, many=True)
        hints_serializer.is_valid()
        return Response(hints_serializer.data, status.HTTP_200_OK)

    def post(self, request, game_id, problem_id):
        user = request.user
        question = request.data['question']
        player = Player.objects.get(user=user, game__id=game_id)
        multiple_problem = CometProblem.objects.get(id=problem_id)
        new_hint = Hint(question=question, multiple_problem=multiple_problem, player=player)
        new_hint.save()

        make_transaction(player, f"درخواست راهنمایی برای مسئله‌ی «{multiple_problem.title}»", -50)

        return Response({"message": "راهنمایی شما با موفقیت ثبت شد! منتظر پاسخگویی مسئولین باشید :)"},
                        status.HTTP_200_OK)


class PlayerView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PlayerSerializer

    def get(self, request, game_id):
        user = request.user
        player = user.player_set.filter(game__id=game_id).first()
        if player is None:
            return Response({"message": "بازیکنی یافت نشد"}, status.HTTP_404_NOT_FOUND)
        player_serializer = self.get_serializer(player)
        return Response(player_serializer.data, status.HTTP_200_OK)


class SubjectView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SubjectSerializer

    def get(self, request, game_id):
        queryset = Subject.objects.filter(games__id=game_id)
        serializer = self.get_serializer(data=queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data, status.HTTP_200_OK)


# related to one problem
class PlayerSingleProblemView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PlayerSingleProblemDetailedSerializer
    queryset = ProblemAnswer.objects.all()
    parser_classes = (MultiPartParser,)

    def get(self, request, game_id, problem_id):
        user = request.user
        player = user.player_set.filter(game__id=game_id).first()
        player_single_problem = self.get_queryset() \
            .filter(player=player, problem__id=problem_id).first()
        if player_single_problem is None:
            return Response({"message": "شما دسترسی ندارید!"}, status.HTTP_403_FORBIDDEN)

        player_problem_serializer = self.get_serializer(player_single_problem)
        return Response(player_problem_serializer.data, status.HTTP_200_OK)

    def post(self, request, game_id, problem_id):
        text_answer, file_answer = request.data['text'], request.FILES.get('file')
        user = request.user
        player = user.player_set.filter(game__id=game_id).first()
        player_single_problem = self.get_queryset() \
            .filter(player=player, problem__id=problem_id, status='RECEIVED').first()
        if player_single_problem is None:
            return Response({"message": "شما دسترسی ندارید!"}, status.HTTP_403_FORBIDDEN)

        player_single_problem.text_answer = text_answer
        player_single_problem.file_answer = file_answer
        player_single_problem.status = 'DELIVERED'
        player_single_problem.save()
        return Response({"message": "پاسخ شما با موفقیت ثبت شد!"}, status.HTTP_200_OK)


# related to one problem
class PlayerMultipleProblemView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProblemDetailedSerializer
    queryset = CometProblemAnswer.objects.all()

    def get(self, request, game_id, problem_id):
        user = request.user
        player = Player.objects.get(game__id=game_id, user=user)
        player_multiple_problem = self.get_queryset() \
            .filter(player=player, multiple_problem__id=problem_id).first()
        if player_multiple_problem is None:
            return Response({"message": "شما دسترسی ندارید!"}, status.HTTP_403_FORBIDDEN)

        multiple_problem_query_set = player_multiple_problem.multiple_problem.problems \
            .order_by('relative_order').all()

        if player_multiple_problem.step == multiple_problem_query_set.count():
            return Response({"status": player_multiple_problem.status}, status.HTTP_200_OK)

        multiple_problem = multiple_problem_query_set[player_multiple_problem.step]
        multiple_problem_serializer = self.get_serializer(multiple_problem)
        return Response(multiple_problem_serializer.data, status.HTTP_200_OK)

    def post(self, request, game_id, problem_id):
        answer = request.data['answer']
        user = request.user
        player = Player.objects.get(game__id=game_id, user=user)
        player_multiple_problem = self.get_queryset() \
            .filter(player=player, multiple_problem__id=problem_id, status='RECEIVED').first()
        if player_multiple_problem is None:
            return Response({"message": "شما دسترسی ندارید!"}, status.HTTP_403_FORBIDDEN)

        multiple_problem_problems = player_multiple_problem.multiple_problem.problems \
            .order_by('relative_order').all()

        if multiple_problem_problems[player_multiple_problem.step].answer == answer:
            player_multiple_problem.step += 1
            player_multiple_problem.save()
            if player_multiple_problem.step == multiple_problem_problems.count():
                player_multiple_problem.status = 'SCORED'
                player_multiple_problem.mark = player_multiple_problem.multiple_problem.reward
                player_multiple_problem.save()
                make_transaction(player,
                                 f"حل‌کردن مسئله‌ی دنباله‌دار «{player_multiple_problem.multiple_problem.title}»",
                                 player_multiple_problem.multiple_problem.reward)
                return Response({"message": "شما این مسئله‌ی دنباله‌دار را با موفقیت حل کردید!"}, status.HTTP_200_OK)
            else:
                return Response({"message": "پاسخ شما درست بود! یک گام به حل دنباله‌دار نزدیک‌تر شدید!"},
                                status.HTTP_200_OK)
        else:
            return Response({"message": "پاسخ شما اشتباه بود!"}, status.HTTP_400_BAD_REQUEST)


# related to problem list
class ProblemView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SingleProblemSerializer
    queryset = ProblemAnswer.objects.all()

    def get(self, request, game_id):
        user = request.user
        player = Player.objects.get(game__id=game_id, users=user)
        query_set = self.get_queryset().filter(player=player)
        serializer = self.get_serializer(data=query_set, many=True)
        serializer.is_valid()
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, game_id):
        print(request.data)
        user, difficulty, subject_id = request.user, request.data['difficulty'], request.data['subject']

        if subject_id is None or difficulty is None:
            return Response({"message": "لطفاً تمام مشخصات خواسته‌شده را وارد کنید!"}, status.HTTP_404_NOT_FOUND)

        player = Player.objects.get(game__id=game_id, users__in=[user])

        received_problems_count = ProblemAnswer.objects.filter(player=player, status='RECEIVED').count()

        game = Game.objects.get(id=game_id)
        if received_problems_count >= game.maximum_number_of_received_problem:
            return Response({
                "message": f"شما نمی‌توانید در یک لحظه بیش از {game.maximum_number_of_received_problem} سوال گرفته‌شده "
                           f" داشته باشید!"}, status.HTTP_400_BAD_REQUEST)

        player_problems = self.get_queryset().filter(player=player).values_list('problem', flat=True)
        available_problems = Problem.objects.filter(games__in=[game], difficulty=difficulty, subject__id=subject_id, ) \
            .exclude(id__in=player_problems.all())

        if available_problems.count() == 0:
            return Response({"message": "شما تمام سوالات این بخش را گرفته‌اید!"}, status.HTTP_404_NOT_FOUND)

        selected_problem = get_random(available_problems)
        new_player_problem = ProblemAnswer(player=player, problem=selected_problem)
        new_player_problem.save()
        make_transaction(player, f'دریافت مسئله‌ی {selected_problem.title}', -selected_problem.cost)

        player_problem_serializer = self.get_serializer(new_player_problem)
        return Response(player_problem_serializer.data, status.HTTP_200_OK)


#  related to problem list
class MultipleProblemView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MultipleProblemSerializer
    queryset = CometProblemAnswer.objects.all()

    def get(self, request, game_id):
        user = request.user
        player = Player.objects.get(game__id=game_id, user=user)
        query_set = self.get_queryset().filter(player=player)
        serializer = self.get_serializer(data=query_set, many=True)
        serializer.is_valid()
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, game_id):
        user = request.user
        player = Player.objects.get(game__id=game_id, user=user)

        received_problems_count = ProblemAnswer.objects.filter(player=player, status='RECEIVED').count()
        received_problems_count += CometProblemAnswer.objects.filter(player=player, status='RECEIVED').count()
        game = Game.objects.get(id=game_id)
        if received_problems_count >= game.maximum_number_of_received_problem:
            return Response({
                "message": f"شما نمی‌توانید در یک لحظه بیش از {game.maximum_number_of_received_problem} سوال گرفته‌شده داشته باشید!"},
                status.HTTP_400_BAD_REQUEST)

        player_multiple_problems = self.get_queryset().filter(player=player).values_list('multiple_problem', flat=True)
        available_problems = CometProblem.objects.all().exclude(id__in=player_multiple_problems.all())
        if available_problems.count() == 0:
            return Response({"message": "شما تمام سوالات این بخش را گرفته‌اید!"}, status.HTTP_404_NOT_FOUND)

        selected_problem = get_random(available_problems)
        new_player_multiple_problem = CometProblemAnswer()
        new_player_multiple_problem.player = player
        new_player_multiple_problem.multiple_problem = selected_problem
        new_player_multiple_problem.game = Game.objects.get(id=game_id)
        new_player_multiple_problem.save()
        make_transaction(player, f'دریافت مسئله‌ی {selected_problem.title}', -selected_problem.cost)
        return Response({"message": "سوال دنباله‌دار با موفقیت اضافه شد!"}, status.HTTP_200_OK)


class PlayerSingleProblemCorrectionView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PlayerSingleProblemCorrectionSerializer
    queryset = ProblemAnswer.objects.all()

    def get(self, request):
        answers = self.get_queryset().filter(status='DELIVERED')
        if answers.count() == 0:
            return Response({"message": "سوال تصحبح‌نشده‌ای باقی نمانده"}, status.HTTP_200_OK)
        selected_answer = get_random(answers)
        serializer = self.get_serializer(selected_answer)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        player_single_problem_id, mark = request.data['player_single_problem_id'], request.data['mark']
        player_single_problem = self.get_queryset().get(id=player_single_problem_id)
        player_single_problem.mark = int(mark) * int(player_single_problem.problem.reward) // 10
        player_single_problem.status = 'SCORED'
        player_single_problem.save()
        make_transaction(player_single_problem.player, f"حل‌کردن مسئله‌ی تکی «{player_single_problem.problem.title}»",
                         player_single_problem.mark)
        return Response({"message": "نمره‌ی این مسئله با موفقیت ثبت شد!"})


class HintAnswering(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = HintAnsweringSerializer
    queryset = Hint.objects.all()

    def get(self, request):
        hints = self.get_queryset().filter(is_answered=False)
        if hints.count() == 0:
            return Response({"message": "همه‌ی راهنمایی‌ها پاسخ داده‌شده‌اند!"}, status.HTTP_200_OK)
        selected_hint = get_random(hints)
        player_questioned_problem = CometProblemAnswer.objects.get(
            multiple_problem=selected_hint.multiple_problem, player=selected_hint.player)

        hint_serializer = self.get_serializer(selected_hint)
        questioned_problem = selected_hint.multiple_problem.problems.all()[player_questioned_problem.step]
        problem_serializer = ProblemDetailedSerializer(questioned_problem)
        return Response({'hint': hint_serializer.data, "questioned_problem": problem_serializer.data},
                        status.HTTP_200_OK)

    def post(self, request):
        hint_id, answer = request.data['hint_id'], request.data['answer']
        hint = self.get_queryset().get(id=hint_id)
        hint.answer = answer
        hint.is_answered = True
        hint.save()
        return Response({"message": "پاسخ راهنمایی با موفقیت ثبت ‌شد!"})


def get_random(query_set):
    pks = query_set.values_list('pk', flat=True).order_by('id')
    random_pk = choice(pks)
    return query_set.get(pk=random_pk)


def make_transaction(player: Player, title: str, value: int):
    player.score += value
    player.save()

    new_transaction = Transaction()
    new_transaction.player = player
    new_transaction.title = title
    new_transaction.amount = value

    new_transaction.save()
