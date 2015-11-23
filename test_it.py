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
from jinja2_s3loader import S3loader
from jinja2 import Environment, Template, TemplateNotFound

import pytest


def test_template_not_found():
    j2 = Environment(loader=S3loader('bluebucket.mindvessel.net'))
    with pytest.raises(TemplateNotFound):
        j2.get_template('nope')


# Note: This is a poor test, because it actually accesses S3,
# and will fail when I remove that specific file (as I am sure to do).
# What can I say, I was in a hurry. – Vince
def test_template():
    j2 = Environment(loader=S3loader('bluebucket.mindvessel.net'))
    t = j2.get_template('_templates/test_template.j2')
    assert isinstance(t, Template)
    print(t.render({}))


def test_prefix():
    j2 = Environment(loader=S3loader('bluebucket.mindvessel.net', '_templates'))
    t = j2.get_template('test_template.j2')
    assert isinstance(t, Template)
    print(t.render({}))

