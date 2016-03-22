#!/usr/bin/env python
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
from jinja2_s3loader import S3loader, gzip
from jinja2 import Environment, Template, TemplateNotFound
from io import BytesIO

from botocore.exceptions import ClientError
import pytest
try:
    import mock
except ImportError:
    import unittest.mock as mock


def test_template_not_found():
    s3 = mock.Mock()
    s3.get_object.side_effect = ClientError({'Error': {}}, 'NoSuchKey')
    j2 = Environment(loader=S3loader('test-bucket', s3=s3))
    with pytest.raises(TemplateNotFound):
        j2.get_template('nope')


# For some reason, the loader gets called twice. The bytesIO does not reset
# itself between. Therefore, we need multiple return values with separate
# objects.
def test_template():
    s3 = mock.Mock()
    body1 = {'Body': BytesIO(b'jinja_template')}
    body2 = {'Body': BytesIO(b'jinja_template')}
    s3.get_object.side_effect = [body1, body2]
    j2 = Environment(loader=S3loader('test-bucket', s3=s3))
    tpl = '_templates/test_template.j2'
    t = j2.get_template(tpl)
    assert isinstance(t, Template)
    assert s3.get_object.called_once_with(Bucket='test-bucket', Key=tpl)
    assert t.render({}) == 'jinja_template'


def test_prefix():
    s3 = mock.Mock()
    body1 = {'Body': BytesIO(b'jinja_template')}
    body2 = {'Body': BytesIO(b'jinja_template')}
    s3.get_object.side_effect = [body1, body2]
    j2 = Environment(loader=S3loader('test-bucket', '_templates', s3=s3))
    t = j2.get_template('test_template.j2')

    tpl = '_templates/test_template.j2'
    assert isinstance(t, Template)
    assert s3.get_object.called_once_with(Bucket='test-bucket', Key=tpl)
    assert t.render({}) == 'jinja_template'


def test_gzip_encoding():
    s3 = mock.Mock()
    body1 = {'Body': BytesIO(gzip(b'jinja_template')),
             'ContentEncoding': 'gzip'}
    body2 = {'Body': BytesIO(gzip(b'jinja_template')),
             'ContentEncoding': 'gzip'}
    s3.get_object.side_effect = [body1, body2]
    j2 = Environment(loader=S3loader('test-bucket', s3=s3))
    tpl = '_templates/test_template.j2'
    t = j2.get_template(tpl)
    assert isinstance(t, Template)
    assert s3.get_object.called_once_with(Bucket='test-bucket', Key=tpl)
    assert t.render({}) == 'jinja_template'

