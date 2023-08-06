from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='actedu-crawler',
    version='1.0.0',
    description='Crawl ACT Education websites\' searchable documents for archival purposes.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/king-millez/actedu-crawler',
    author='king-millez',
    author_email='millez.dev@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    python_requires='>=3.6'
)