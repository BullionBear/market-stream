from setuptools import setup, find_packages

setup(
    name='market-stream',
    version='0.0.3',
    description='A centralized market stream manager',
    author='Yi Te',
    author_email='coastq22889@icloud.com',
    packages=find_packages(include=['market_stream', 'generated', "helper"]),
    install_requires=[
        'websockets',
        'redis',
        'aioredis'
    ],
)
