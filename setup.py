from os import path

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'VERSION')) as f:
    version = f.read().strip()

setup(
        name='aerender',
        version=version,
        description='asyncio wrapper for Adobe After Effects aerender',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/devtud/aerender',
        author='devtud',
        author_email='devtud@gmail.com',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.7',
        ],
        keywords='asyncio async aerender',
        packages=find_packages(exclude=['contrib', 'docs', 'tests']),
        python_requires='>=3.7, <4',
        project_urls={
            'Source': 'https://github.com/devtud/aerender',
        },
)
