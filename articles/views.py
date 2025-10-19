# articles/views.py
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import PostSerializer

class ArticleListCreate(APIView):
    """
    GET  /article/?limit=10&offset=0
    POST /article/
    """
    def get(self, request):
        # ambil query param
        try:
            limit = int(request.query_params.get("limit", 10))
            offset = int(request.query_params.get("offset", 0))
        except ValueError:
            return Response(
                {"detail": "limit dan offset harus berupa angka integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # jaga nilai agar aman
        if limit < 1:  limit = 1
        if limit > 100: limit = 100     # hard cap agar tidak terlalu berat
        if offset < 0: offset = 0

        qs = Post.objects.all()
        items = qs[offset:offset + limit]
        data = PostSerializer(items, many=True).data

        return Response({
            "count": qs.count(),
            "limit": limit,
            "offset": offset,
            "results": data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        ser = PostSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetail(APIView):
    """
    GET/PUT/PATCH/DELETE /article/<id>
    """
    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)

    def get(self, request, pk):
        return Response(PostSerializer(self.get_object(pk)).data)

    def put(self, request, pk):
        post = self.get_object(pk)
        ser = PostSerializer(post, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        post = self.get_object(pk)
        ser = PostSerializer(post, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
