==============================================================
jinja2_s3loader: A Jinja2 template loader for AWS S3.
==============================================================

**Project Status:** Beta. It's pretty simple and works for me, but not heavily
tested in production use. Caveat Emptor.

Usage
--------------------------------

This library relies on the `boto3`_ library for S3 access, so you will need to
`configure your AWS credentials`_ first. Then, provide your S3 bucket name when
instantiating the loader::

    from jinja2 import Environment
    from jinja2_s3loader import S3loader

    j2 = Environment(loader=S3loader('my-s3-bucket-name'))
    t = j2.get_template('mytemplate.j2')
    print(t.render({}))

.. _boto3: https://boto3.readthedocs.org/en/latest/index.html
.. _configure your AWS credentials: https://boto3.readthedocs.org/en/latest/guide/configuration.html

Remember, accessing files over S3 costs money. The loader currently does not
support live reloading. I built this to support accessing S3 templates from AWS
Lambda functions, so those constraints are fine with me, but your use case may
be different. Contributions welcome. File a Github issue to report a bug.

License
--------------------------------

Copyright 2015 Vince Veselosky and contributors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
