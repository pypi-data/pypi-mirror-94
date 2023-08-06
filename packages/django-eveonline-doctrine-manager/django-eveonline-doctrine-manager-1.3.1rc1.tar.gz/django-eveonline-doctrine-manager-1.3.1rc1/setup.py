import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-eveonline-doctrine-manager',
    version=__import__('django_eveonline_doctrine_manager').__version__,
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A simple Django package.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/KryptedGaming/django-eveonline-doctrine-manager.git',
    author='django_eveonline_doctrine_manager',
    author_email='porowns@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'roman',
        'django_eveonline_connector',
        'django-crispy-forms',
        'django-singleton-admin-2',
    ]
)
