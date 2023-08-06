from setuptools import setup


setup(
    name='snotomo',
    version='0.1.0',    
    description='A package for interacting with the Tomo Snowflake data warehouse',
    url='https://github.com/TomoNetworks/snotomo',
    author='Colin Bradley',
    author_email='colin@tomonetworks.com',
    license='MIT License',
    packages=['snotomo'],
    install_requires=[
                      'numpy',   
                      'SQLAlchemy',
                      'snowflake-connector-python'                 
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',  
        'Programming Language :: Python :: 3.8',
    ],
)