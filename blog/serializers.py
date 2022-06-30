from rest_framework import serializers, validators
from .models import User, Enquire
import re


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', "role")

        extra_kwargs = {
            "password": {"write_only": True},
            "role": {"required": False},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), "A user with that Email already exists"
                    )
                ]
            }
        }

    def validate_password(self, value):

        total_digits = len(re.findall('[0-9]', value))
        total_letters = len(re.findall('[A-z]', value))
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

        special_char = 0
        for i in range(0, len(value)):

            if value[i].isalpha():
                continue
            elif value[i].isdigit():
                continue
            else:
                special_char += 1

        if special_char < 2:
            raise serializers.ValidationError('Password should be contain minimum of 2 special chars')

        if total_letters < 8:
            raise serializers.ValidationError('Password should be contain minimum of 8 letters')
        if total_digits < 2:
            raise serializers.ValidationError('Password should be contain minimum of 2 numbers')
        return value

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        role = validated_data.get('role')
        user = User.objects.create(username=username, email=email, password=password, role=role)
        return user


class EnquireListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquire
        fields = '__all__'
