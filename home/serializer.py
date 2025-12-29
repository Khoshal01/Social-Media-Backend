from rest_framework import serializers
from django.contrib.auth.models import User,Group
from django.contrib.auth.password_validation import validate_password
from home.model import Profile, Follow , PostModel , Comment

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 100)
    password = serializers.CharField(
    )
    
    class Meta:
        model  = User 
        fields = ['username','password']

    def validate(self,data):
        
        if not User.objects.filter(email = data['username']).exists():
            raise serializers.ValidationError({'username':'username Does Not Exists'})
        
        return data 

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 100)
    email = serializers.EmailField(required = True)
    password = serializers.CharField(
        write_only = True,
        required = True ,
        validators = [validate_password]
    )

    password_again = serializers.CharField(
        write_only = True,
        required = True
    )

    def validate(self,data):
        if data['password'] != data['password_again']:
            raise serializers.ValidationError({"password": "Passwords don't match"})
        
        if User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError({'username':'Username arlready Exists'})
        
        if User.objects.filter(email = data['email']).exists():
            raise serializers.ValidationError({'Email':'Email arlready Exists'})
        
        return data 
    

    def create(self,data):
        data.pop('password_again')

        try:

            user = User.objects.create_user(username = data['username'],email = data['email'])
            user.set_password(data['password'])
            user.save()

        except Exception:
            raise serializers.ValidationError("User did not create, Try again! ")

        return user 
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta :
        model = Profile
        fields = ['bio','is_private','followers_count', 'following_count']

    def validate(self,validated_data):
        request = self.context.get('request')
        user = request.user
        if Profile.objects.filter(user = user).exists():
            raise serializers.ValidationError("User already has a Profile")

        return validated_data
    
    def create(self, validated_data):
        user = self.context['request'].user  # User instance
        profile = Profile.objects.create(user=user, **validated_data)
        profile.save()
        return profile


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source = 'user.user.username',read_only = True)
    class Meta:
        model = Comment
        fields = ['id', 'user_name', 'text', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = PostModel
        fields = ['id','content','privacy','likes_count', 'comments_count','comments']
        read_only_fields = ['id', 'likes_count', 'comments_count','comments']
    
    
