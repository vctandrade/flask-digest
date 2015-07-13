from setuptools import setup, find_packages

setup(
    name = 'Flask-Digest',
    version = '0.1.0',

    author = 'Victor Andrade de Almeida',
    author_email = 'vct.a.almeida@gmail.com',
    url = 'https://github.com/vctandrade/flask-digest',

    description = 'A RESTful authentication service for Flask applications',
    long_description = open('README.rst').read(),
    license = 'MIT',

    platforms = ['Platform Independent'],
    install_requires = ['Flask >= 0.10.1'],
    packages = find_packages(),

    keywords = ['digest', 'authentication', 'flask'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation'
    ]
)
