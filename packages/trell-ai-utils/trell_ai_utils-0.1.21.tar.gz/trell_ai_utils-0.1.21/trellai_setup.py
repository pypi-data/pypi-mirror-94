"""Setup for the chocobo package."""

import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Abhay Kumar",
    author_email="abhay@trell.in",
    name='trell_ai_utils',
    description='Utility code for trell ai repos',
    version='v0.1.21',
    long_description=README,
    url='https://gitlab.com/abhay7/trell-ai-util',
    packages=setuptools.find_packages(),
    python_requires=">=3.6.9",
    install_requires=['requests','emoji','json-utils', 'python-dotenv', 'pandas_gbq',
                      'google-cloud', 'google-cloud-bigquery', 'mysql-connector',
                        'mysql-replication', "subprocess32", "psutil",
                      "Flask", "SQLAlchemy", "SQLAlchemy-JSONField",
                      "SQLAlchemy-Utils", "boto","boto3",
                      ],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'

    ],
)


