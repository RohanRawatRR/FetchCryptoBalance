from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from user.helper import Web3Helper


class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "password", "password2", "ethereum_wallet_address")
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True}
        }

    def save(self):
        user = get_user_model()(
            email=self.validated_data["email"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            ethereum_wallet_address=self.validated_data['ethereum_wallet_address']
        )

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError(
                {"password": "Passwords do not match!"})

        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    '''
        User serializer to fetch the user details along with
        Ethereum Wallet balance.
    '''
    ethereum_wallet_balance = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "is_staff", "first_name", "last_name", "ethereum_wallet_address", "ethereum_wallet_balance")
    
    def get_ethereum_wallet_balance(self, obj):
        # Fetching ethereum wallet balance using wallet address.
        try:
            balance = Web3Helper.fetch_ethereum_balance(obj.ethereum_wallet_address)
        except Exception as e:
            # Printing exception and sending 0 as the balance.
            print(e)
            balance = 0
        return balance
