# Copyright 2020 The T5 Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Install T5."""

import os
import sys
import setuptools

# To enable importing version.py directly, we add its path to sys.path.

setuptools.setup(
    name='seqio',
    version='0.0.0',
    description='SeqIO',
    author='Google Inc.',
    author_email='no-reply@google.com',
    url='http://github.com/google-research/text-to-text-transfer-transformer',
    license='Apache 2.0',
    packages=setuptools.find_packages(),
    scripts=[],
    install_requires=[
        'absl-py',
        'numpy',
        'scipy',
        'sentencepiece',
        'tensorflow-text',
        'tfds-nightly',
    ],
    extras_require={
        'cache-tasks': ['apache-beam'],
        'test': ['pytest'],
    },
    entry_points={},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='text nlp machinelearning',
)
