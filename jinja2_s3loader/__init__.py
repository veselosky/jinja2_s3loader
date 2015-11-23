# -*- coding: utf-8 -*-
# Copyright 2015 Vince Veselosky and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import, print_function
from jinja2 import BaseLoader, TemplateNotFound
from botocore.exceptions import ClientError
import boto3
import posixpath as path


class S3loader(BaseLoader):
    s3 = boto3.client('s3')

    def __init__(self, bucket, prefix=''):
        self.bucket = bucket
        self.prefix = prefix
        super(S3loader, self).__init__()

    def get_source(self, environment, template):
        if self.prefix:
            template = path.join(self.prefix, template)
        try:
            resp = self.s3.get_object(Bucket=self.bucket, Key=template)
        except ClientError as e:
            if "NoSuchKey" in e.__str__():
                raise TemplateNotFound(template)
            else:
                raise e
        return (resp['Body'].read().decode('utf-8'), None, lambda: True)

