from setuptools import setup


setup(
    name='Flask-MSTrans',
    version='0.1',
    url='https://github.com/osleg/Flask-MsTranslate/archive/master.zip',
    license='BSD',
    author='Alex Kir',
    author_email='alex@wall-dev.org',
    description='Translate text using Bing',
    long_description=__doc__,
    py_modules=['flask_mstrans'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)