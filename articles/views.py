
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ArticleSerializer, ArticleDetailSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Article , Comment


class ArticleListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Articles"],
        description="Article 목록 조회를 위한 API",
    )
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=["Articles"],
        description="Article 생성을 위한 API",
        request=ArticleSerializer,
    )
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        data = {"pk": f"{pk} is deleted."}
        return Response(data, status=status.HTTP_200_OK)


class CommentListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        comments = article.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, comment_pk):
        return get_object_or_404(Comment, pk=comment_pk)

    def delete(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        comment.delete()
        data = {"pk": f"{comment_pk} is deleted."}
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(["GET"])
def check_sql(request):

    comments = Comment.objects.all().prefetch_related
    for comment in comments:
        print(comment.article.title)

    return Response()