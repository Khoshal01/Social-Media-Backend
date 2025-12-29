from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token 
from rest_framework import status, viewsets
from home.serializer import RegisterSerializer , ProfileSerializer , PostSerializer
from home.service import ProfileServices , Follow , PostServices , LikeService , CommentService
from home.model import Profile , PostModel

# ======================
# Login View
# ======================

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username = username, password = password)

        if not user:
            return Response({
                'message':'No user with this username',
                'status':404
                })
        
        refresh_token = RefreshToken.for_user(user)

        return Response({
            'message':'Welcome!',
            'refresh_token':str(refresh_token),
            'access_token':str(refresh_token.access_token)

        })
    

# ======================
# Register View
# ======================
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = RegisterSerializer(data = request.data )

        if serializer.is_valid():
            user = serializer.save()

            refresh_token = RefreshToken.for_user(user)

            return Response({
                'message':'User Created',
                'refresh_token':str(refresh_token),
                'access_token':str(refresh_token.access_token)
            })


# ======================
# Profile view
# ======================
class ProfileModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user = self.request.user)
    
    def perform_create(self,serializer):
        user = self.request.user
       
        bio = serializer.validated_data.get('bio')
        image = serializer.validated_data.get('image')
        is_private = serializer.validated_data.get('is_private')

        profile = ProfileServices.create_profile(
            user = user,
            bio = bio,
            image=  image,
            is_private= is_private
        )

        return profile
    
# ======================
# Post view
# ======================


class PostModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    #lookup_field = 'id'

    queryset = PostModel.objects.all()
    
    def perform_create(self,serializer):
        post = PostServices.create_post(
        author=self.request.user.profile,
        content=serializer.validated_data['content'],
        media_url=serializer.validated_data.get('media_url'),
        privacy=serializer.validated_data['privacy']
        )
        serializer.instance = post

    @action(detail=True, methods=['post'], url_path='like')
    def like(self, request, pk=None):
        post = self.get_object()
        LikeService.like_post(user_profile=request.user.profile, post=post)
        return Response({"detail": "Post liked"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='unlike')
    def unlike(self, request, pk=None):
        post = self.get_object()
        LikeService.unlike_post(user_profile=request.user.profile, post=post)
        return Response({"detail": "Post unliked"}, status=status.HTTP_200_OK)
    
    @action(detail = True, methods=['post'], url_path='comment')
    def post_comment(self,request,pk=None):
        post = self.get_object()
        text = request.data.get('comment')
        CommentService.post_comment(user_profile=request.user.profile,post = post,comment=text)
        return Response({'Detail':'Comment Posted'})
    
    @action(detail = True, methods = ['post'], url_path = 'deleteComment')
    def delete_comment(self,request,pk=None):
        post = self.get_object()
        CommentService.delete_post(user_profile=request.user.profile,post=post)
        return Response({'Detail':'Comment Deleted'})
    
        

    





# ======================
# Follow View
# ======================
class FollowViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        username = request.data.get('username')
        try:
            target_username = User.objects.get(username = username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        
        if target_username == request.user:
            return Response({"error": "Cannot follow yourself"}, status=400)

        follow , created = Follow.objects.get_or_create(
            follower = request.user,
            following = target_username,
        )

        if not created:
            follow.delete()
            return Response({"message": "Unfollowed successfully"})
        return Response({"message": "Followed successfully"})

