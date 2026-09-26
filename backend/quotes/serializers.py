from rest_framework import serializers

from .models import QuoteRequest, QuoteAttachment


class QuoteRequestSerializer(serializers.ModelSerializer):

    files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )


    class Meta:
        model = QuoteRequest

        fields = [
            'id',

            'first_name',
            'last_name',
            'email',
            'phone',
            'service',

            'pickup_address',
            'pickup_city',
            'pickup_postal_code',
            'pickup_floor',
            'pickup_elevator',

            'destination_address',
            'destination_city',
            'destination_postal_code',
            'destination_floor',
            'destination_elevator',

            'preferred_date',
            'items',
            'notes',

            'consent_accepted',

            'files',

            'created_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
        ]


    def validate_consent_accepted(self, value):

        if not value:
            raise serializers.ValidationError(
                'You must accept the privacy policy.'
            )

        return value


    def validate_files(self, files):

        allowed_types = [
            'image/jpeg',
            'image/png',
            'image/webp',
            'video/mp4',
        ]

        max_size = 25 * 1024 * 1024


        for uploaded_file in files:

            if uploaded_file.size > max_size:
                raise serializers.ValidationError(
                    f'{uploaded_file.name} is larger than 25 MB.'
                )


            if uploaded_file.content_type not in allowed_types:
                raise serializers.ValidationError(
                    f'{uploaded_file.name} has an unsupported file type.'
                )


        return files


    def create(self, validated_data):

        files = validated_data.pop(
            'files',
            []
        )


        quote = QuoteRequest.objects.create(
            **validated_data
        )


        for uploaded_file in files:

            QuoteAttachment.objects.create(
                quote=quote,
                file=uploaded_file,
                original_name=uploaded_file.name,
                content_type=uploaded_file.content_type,
                file_size=uploaded_file.size,
            )


        return quote
