from rest_framework import serializers
from .models import ContactRequest


class ContactRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactRequest

        fields = [
            'id',
            'name',
            'email',
            'phone',
            'message',
            'consent_accepted',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
        ]

    def validate_consent_accepted(self, value):
        if not value:
            raise serializers.ValidationError(
                "You must accept the privacy policy."
            )

        return value
