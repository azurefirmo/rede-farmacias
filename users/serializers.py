from rest_framework import serializers
from .models import User

# Create your models here.

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'email', 'role',
            'cpf_cnpj', 'phone', 'crf_number', 'crf_state', 'branch'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Criptografa a senha ao criar o usuário
        user = User.objects.create_user(**validated_data)
        return user