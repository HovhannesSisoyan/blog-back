from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    @action(detail=True, methods=['POST'])
    def add_comment(self, request, pk=None):
        if 'text' in request.data:
            post = Post.objects.get(id=pk)
            text = request.data['text']
            user = request.user
            comment = Comment(
                text=text,
                post=post,
                user=user
            )
            comment.save()
            serializer = CommentSerializer(comment, many=False)
            response = {
                'message': 'comment added',
                'result': serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'you need to provide text'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
