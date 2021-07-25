import re
from django.shortcuts import render
from rest_framework import generics,mixins, pagination
from .models import Ebook,Review
from .serializers import EbookSerializer,ReviewSerializer
from rest_framework import permissions
from .permissions import IsAdminUserOrReadOnly,IsReviewAuthorOrReadOnly
from rest_framework.exceptions import ValidationError
from .pagination import SmallSetPagination

# Create your views here.

# class EbookListCreateAPIView(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset=Ebook.objects.all()
#     serializer_class=EbookSerializer

#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)

class EbookListCreateAPIView(generics.ListCreateAPIView):
    queryset=Ebook.objects.all().order_by("-id")
    serializer_class=EbookSerializer
    permission_classes=[IsAdminUserOrReadOnly]
    pagination_class=SmallSetPagination


class EbookDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset=Ebook.objects.all()
    serializer_class=EbookSerializer
    permission_classes=[IsAdminUserOrReadOnly]

    # def get(self, request, *args, **kwargs):
    #     print("hello world")
    #     # print(self.kwargs['pk'])
    #     return super().get(request, *args, **kwargs)

class ReviewCreateAPIView(generics.CreateAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer

    def perform_create(self, serializer):
        # print("create")
        # print("hello world")
        # print(self.kwargs)
        ebook_pk=self.kwargs.get("ebook_pk")
        ebook=generics.get_object_or_404(Ebook,pk=ebook_pk)

        review_author=self.request.user
        review_queryset=Review.objects.filter(ebook=ebook,review_author=review_author)
        if(review_queryset.exists()):
            raise ValidationError("you Have Already Reviewed this Ebook!")

        serializer.save(ebook=ebook,review_author=review_author)

class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[IsReviewAuthorOrReadOnly]



