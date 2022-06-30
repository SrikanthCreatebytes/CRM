from django.contrib.auth import authenticate
from django.shortcuts import render
from django.db.models import Q
from rest_framework.authentication import TokenAuthentication

from .models import Enquire
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK

from .models import User
from .serializers import RegisterSerializer, EnquireListSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import status
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.views import APIView


@api_view(['POST'])
def register_api(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response(
            {"message": status.HTTP_201_CREATED,
             "username": user.username,
             "email": user.email,
             "token": token.key
             }
        )


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    if username and password:
        try:
            user = User.objects.get(username=username, password=password)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key},
                            status=HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Invalid Credentials'},
                            status=HTTP_404_NOT_FOUND)


class EnquireListAPiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, status):
        space = request.GET.get('status')
        if space == 'public':
            enquiry_set = Enquire.objects.filter(claimed_by__null=True)
        elif space == 'private':
            enquiry_set = Enquire.objects.filter(claimed_by=request.user)
        else:
            enquiry_set = Enquire.objects.all()
        serializer = EnquireListSerializer(enquiry_set, many=True)

        return Response(serializer.data)




