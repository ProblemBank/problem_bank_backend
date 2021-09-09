from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get(request):
    user = request.user
    player = user.player_set.first()
    player.has_find_TABOOT = True
    player.save()
    from rest_framework import status
    return Response({'message': 'تبریک! شما تابوت توتنخ‌عامو را پیدا کردید! به همین خاطر '}, status=status.HTTP_200_OK)

