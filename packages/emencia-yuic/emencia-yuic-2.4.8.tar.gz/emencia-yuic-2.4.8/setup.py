from setuptools import setup, find_packages

setup(
    name='emencia-yuic',
    version=__import__('yuicompressor').__version__,
    description="Nope",
    long_description="Niet",
    long_description_content_type="text/x-rst",
    author='Emencia',
    author_email='support@emencia.com',
    url='http://perdu.com',
    license='Proprietary License',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[],
    extras_require={
        'dev': [
            'pytest>=4.6.11,<5.0.0',
            'webassets==0.8',
            'twine==1.15.0',
        ]
    },
    entry_points={
        'console_scripts': [
            'yuicompressor = yuicompressor:main',
        ]
    },
    include_package_data=True,
    zip_safe=False
)
