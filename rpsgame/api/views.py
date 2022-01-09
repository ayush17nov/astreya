from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import GameUserSerializer
from .models import GameUser 


class GameUsersAPIView(APIView):

    def get(self, request):
        users = GameUser.objects.all()
        serializer = GameUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            GameUser.objects.get(name=request.data["name"])
        except GameUser.DoesNotExist:
            serializer = GameUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User Saved Successfully."}, status.HTTP_201_CREATED)
            else:
                return Response({"message": "data provided is not valid."}, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "user already exists."}, status.HTTP_302_FOUND)

    def delete(self, request):
        try:
            user = GameUser.objects.get(name=request.data["name"])
        except GameUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({"message": "user deleted successfully"})
