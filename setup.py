from setuptools import setup

setup(name='Sample django 1.6 on Red Hat Openshift',
    version='1.0',
    description='OpenShift App',
    author='Your Name',
    author_email='example@example.com',
    url='http://www.python.org/sigs/distutils-sig/',
    install_requires=['Django>=1.6', 'Django<1.7'
    'django-widget-tweaks>=1.3,<1.4',
    'djangorestframework>=2.3,<2.4',
    'requests>=2.3,<2.4',
    'coverage>=3.7,<3.8',],
)
