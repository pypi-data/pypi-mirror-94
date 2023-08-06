#
#   Thiscovery API - THIS Institute’s citizen science platform
#   Copyright (C) 2019 THIS Institute
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   A copy of the GNU Affero General Public License is available in the
#   docs folder of this project.  It is also available www.gnu.org/licenses/
#
import thiscovery_lib.utilities as utils


class S3Client(utils.BaseClient):

    def __init__(self, profile_name=None):
        super().__init__('s3', profile_name=profile_name)

    def list_objects(self, bucket, **kwargs):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects_v2
        """
        return self.client.list_objects_v2(
            Bucket=bucket,
            **kwargs
        )

    def get_object(self, bucket, key, **kwargs):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object
        """
        return self.client.get_object(
            Bucket=bucket,
            Key=key,
            **kwargs
        )

    def head_object(self, bucket, key, **kwargs):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.head_object
        """
        return self.client.head_object(
            Bucket=bucket,
            Key=key,
            **kwargs
        )

    def download_fileobj(self, bucket, key, file_obj, **kwargs):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.download_fileobj
        """
        return self.client.download_fileobj(
            Bucket=bucket,
            Key=key,
            Fileobj=file_obj,
            **kwargs
        )

    def delete_objects(self, bucket, keys, **kwargs):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_objects

        Args:
            bucket:
            keys (list): keys of objects to be deleted
            **kwargs:

        Returns:
        """
        return self.client.delete_objects(
            Bucket=bucket,
            Delete={
                'Objects': [{'Key': x} for x in keys],
            },
            **kwargs
        )
