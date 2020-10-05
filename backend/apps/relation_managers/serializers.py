from rest_framework import serializers

class UserRelationSerializerField(serializers.SerializerMethodField):



class UserRelationSerializerMixin(serializers.ModelSerializer):
    user_relation =

