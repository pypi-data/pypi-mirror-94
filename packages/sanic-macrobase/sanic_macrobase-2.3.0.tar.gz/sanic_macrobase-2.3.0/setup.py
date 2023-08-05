from setuptools import setup, find_packages

setup(
    name='sanic_macrobase',
    version='2.3.0',
    packages=find_packages(),
    url='https://github.com/mbcores/sanic-macrobase',
    license='MIT',
    author='Alexey Shagaleev',
    author_email='alexey.shagaleev@yandex.ru',
    description='Sanic driver for macrobase framework',
    install_requires=[
        'macrobase-driver>=2.0.0,<3.0.0',
        'sanic==18.12.0',
        'structlog==19.2.0',
        'sentry-sdk>=0.14.3',
        'aiocontextvars==0.2.2'
    ]
)
