from setuptools import setup, find_packages
import os

current_folder = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_folder, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='theos',
    version='0.0.1',
    description='A cross-platform suite of tools for building and deploying software for iOS and other platforms.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/theos/theos',
    author='theos',
    author_email='web@theos.dev',
    license='GPL v3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='theos',
    packages=find_packages(exclude='tests'),
    python_requires='>=3.6',
    project_urls={
        'Funding': 'https://donate.pypi.org',
        'Documentation': r'https://github.com/theos/theos'
    },
)
