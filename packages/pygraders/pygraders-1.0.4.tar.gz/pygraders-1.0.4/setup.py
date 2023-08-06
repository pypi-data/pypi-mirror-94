'''
Copyright 2018-2020 Autograders.org

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
import pathlib
import setuptools

# README.md
README = (pathlib.Path(__file__).parent / "README.md").read_text()

setuptools.setup(
    license='Apache-2.0',
    name='pygraders',
    version='1.0.4',
    author='Andrés Castellanos',
    author_email='andres.cv@galileo.edu',
    description='Autograders Python3 Library',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/autograders/lib/',
    project_urls={
        'Source': 'https://github.com/autograders/lib/',
        'Documentation': 'https://github.com/Autograders/lib/blob/main/README.md'
    },
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    packages=[
        'autograders'
    ],
    python_requires='>=3.6',
    install_requires=[
        'boto3',
        'paramiko'
    ],
    include_package_data=True
)
