from django.db import connection, transaction
from django.utils.html import escape
from django.shortcuts import get_object_or_404


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from .serializer import *


@api_view(['GET'])
@permission_classes([AllowAny])
def list_users(request: Request) -> Response:
    values = UsersSerializer(User.objects, many=True).data
    if values:
        return Response(values, status=status.HTTP_200_OK)
    return Response({"msg": "no users found"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user(request: Request) -> Response:
    values = User.objects.filter(id=request.query_params.get('user_id')).first()
    print(values)
    if values:
        user = UsersSerializer(values).data
        return Response(user, status=status.HTTP_200_OK)
    return Response({"msg": "Usuarios não encontrados"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request: Request) -> Response:
    user = User()

    usuario = escape(request.data.get('usuario'))
    nome = escape(request.data.get('nome'))
    sobrenome = escape(request.data.get('sobrenome'))
    email = escape(request.data.get('email'))
    senha = escape(request.data.get('senha'))


    if not 'usuario' in request.data:
        return Response({"msg": "Favor informar um nome de usuario"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not 'nome' in request.data:
        return Response({"msg": "Favor informar um nome"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not 'email' in request.data:
        return Response({"msg": "Favor informar um email"}, status=status.HTTP_400_BAD_REQUEST)

    if not 'senha' in request.data:
        return Response({"msg": "Favor informar uma senha"}, status=status.HTTP_400_BAD_REQUEST)

    user.username = usuario
    user.first_name = nome
    user.last_name = sobrenome
    user.email = email
    user.set_password(senha)
    user.save()

    return Response({"msg": "Usuario cadastrado com sucesso!"}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_user(request: Request) -> Response:
    User.objects.filter(id=request.query_params.get('user_id')).delete()
    return Response({"msg": "Usuario apagado com sucesso!"}, status=status.HTTP_200_OK)