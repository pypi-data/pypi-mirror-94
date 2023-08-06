
from os import path
from setuptools import setup

current = path.abspath(path.dirname(__file__))

setup(
    name='redis dict',
    author='Melvin Bijman',
    author_email='bijman.m.m@gmail.com',
    version='1.0',
    py_modules=['redis_dict'],
    install_requires=['redis', 'future'],
    license='MIT',

    url='https://github.com/Attumm/redisdict',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',

        'Topic :: Database',
        'Topic :: System :: Distributed Computing',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)

