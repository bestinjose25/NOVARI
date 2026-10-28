import warnings

from django.conf import settings
from django.db import transaction
from PIL import Image, UnidentifiedImageError
from rest_framework import serializers

from .models import QuoteRequest, QuoteAttachment


class QuoteRequestSerializer(serializers.ModelSerializer):
    consent_accepted = serializers.BooleanField(required=True)

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
            'referral_source',

            'consent_accepted',

            'files',

            'created_at',
        ]

        extra_kwargs = {
            'pickup_city': {'required': True, 'allow_blank': False},
            'pickup_postal_code': {'required': True, 'allow_blank': False},
            'pickup_floor': {'required': True, 'allow_blank': False},
            'destination_city': {'required': True, 'allow_blank': False},
            'destination_postal_code': {'required': True, 'allow_blank': False},
            'destination_floor': {'required': True, 'allow_blank': False},
        }

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
        if len(files) > settings.MAX_QUOTE_FILES:
            raise serializers.ValidationError('Upload at most 6 files.')
        if sum(file.size for file in files) > settings.MAX_QUOTE_UPLOAD_BYTES:
            raise serializers.ValidationError('The combined upload size must not exceed 25 MB.')


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


        for uploaded_file in files:
            try:
                uploaded_file.seek(0)
                if uploaded_file.content_type.startswith('image/'):
                    with warnings.catch_warnings():
                        warnings.simplefilter('error', Image.DecompressionBombWarning)
                        with Image.open(uploaded_file) as image:
                            expected = {'image/jpeg': 'JPEG', 'image/png': 'PNG', 'image/webp': 'WEBP'}
                            if image.format != expected[uploaded_file.content_type]:
                                raise ValueError('Image type mismatch')
                            if image.width * image.height > 25_000_000:
                                raise ValueError('Image dimensions exceed limit')
                            image.verify()
                else:
                    # Container signature check, not an antivirus scan/video decode.
                    header = uploaded_file.read(32)
                    if len(header) < 16 or header[4:8] != b'ftyp':
                        raise ValueError('Invalid MP4 container')
            except (OSError, ValueError, SyntaxError, UnidentifiedImageError,
                    Image.DecompressionBombWarning, Image.DecompressionBombError):
                raise serializers.ValidationError(f'{uploaded_file.name} is not a valid supported image or MP4 file.')
            finally:
                uploaded_file.seek(0)

        return files


    def create(self, validated_data):

        files = validated_data.pop(
            'files',
            []
        )


        saved_files = []
        try:
            with transaction.atomic():
                quote = QuoteRequest.objects.create(**validated_data)
                for uploaded_file in files:
                    attachment = QuoteAttachment(
                        quote=quote, original_name=uploaded_file.name,
                        content_type=uploaded_file.content_type, file_size=uploaded_file.size,
                    )
                    attachment.file.save(uploaded_file.name, uploaded_file, save=False)
                    saved_files.append((attachment.file.storage, attachment.file.name))
                    attachment.save()
            return quote
        except Exception:
            # Database rollback does not remove uploaded files.
            for storage, name in saved_files:
                storage.delete(name)
            raise
