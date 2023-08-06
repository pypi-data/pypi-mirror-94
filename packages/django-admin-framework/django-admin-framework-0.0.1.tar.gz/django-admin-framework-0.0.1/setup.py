from setuptools import find_packages, setup

import admin_framework


setup(
    name='django-admin-framework',
    url=admin_framework.__url__,
    version=admin_framework.__version__,
    license=admin_framework.__license__,
    description='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author=admin_framework.__author__,
    author_email=admin_framework.__email__,
    packages=find_packages(exclude=['tests*']),
    project_urls={
        'Source': admin_framework.__url__,
    },
    include_package_data=True,
    zip_safe=True,
    setup_requires='wheel',
    classifiers=[
        'Topic :: Internet :: WWW/HTTP',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 1 - Planning',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only'
    ]
)
