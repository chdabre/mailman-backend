from rest_framework import serializers

from jobs.models import PostcardJob, Address


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'firstname', 'lastname', 'street', 'city', 'zipcode', 'is_primary']


class PostcardJobSerializer(serializers.ModelSerializer):
    front_image = Base64ImageField(max_length=None, use_url=True)
    is_landscape = serializers.SerializerMethodField()

    sender = AddressSerializer(read_only=True)
    sender_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        source='sender',
        queryset=Address.objects.all()
    )

    recipient = AddressSerializer(read_only=True)
    recipient_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        source='recipient',
        queryset=Address.objects.all()
    )

    def get_is_landscape(self, obj):
        if obj.front_image:
            return obj.front_image.width > obj.front_image.height
        else:
            return None

    class Meta:
        model = PostcardJob

        fields = [
            'id',
            'status',
            'send_on',
            'front_image',
            'text_image',
            'message',
            'sender_id',
            'recipient_id',
            'is_landscape',
            'recipient',
            'sender',
            'time_sent',
        ]

        extra_kwargs = {
            'time_sent': {'read_only': True},
            'text_image': {'read_only': True},
        }