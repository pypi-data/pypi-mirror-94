import os
from setuptools import setup


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


setup(
    name='replisync',
    version='0.5.4',
    description='Транслятор репликации в задачи Celery',
    license='MIT',
    author='BARS Group',
    author_email='kirov@bars-open.ru',
    url="https://stash.bars-open.ru/projects/BUDG/repos/replisync",
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
    ],
    packages=['replisync'],
    include_package_data=True,
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=[      
        'psycopg2',
        'celery',
    ],
    entry_points={
        'console_scripts': ['replisync=replisync.start:main'],
    }
)