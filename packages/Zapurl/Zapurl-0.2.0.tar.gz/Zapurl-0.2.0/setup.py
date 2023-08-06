from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Information Technology',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Natural Language :: English'
]

setup(
    name = 'Zapurl',
    version = '0.2.0',
    description = 'A tool that allows you to connect directly to ZapURL to shorten link through Python.',
    long_description_content_type = 'text/markdown',
    long_description = open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    url = '',
    author = 'Jonathan Wang',
    author_email = 'jonathanwang2018@gmail.com',
    License = 'MIT',
    classifiers = classifiers,
    keywords = 'URL, Shortener, ZapURL',
    packages = find_packages(),
    install_requires=['']
)
