import os

from rest_framework import serializers


class CDNFileField(serializers.FileField):
    def to_representation(self, value):
        if not value:
            return None
        file_name = value.name if hasattr(value, 'name') else str(value)
        bucket_url = os.environ.get("S3_BUCKET_URL", "")
        bucket = os.environ.get("S3_BUCKET", "")
        return "https://{}/{}/{}".format(bucket_url, bucket, file_name)
