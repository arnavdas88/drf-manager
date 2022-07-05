import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='DRF Manager',
    version='0.0.1',
    author_email='arnav@zeron.one',
    # scripts=['bin/script1','bin/script2'],
    url='http://pypi.python.org/pypi/drf-manager/',
    project_urls={
        "GitHub": "https://github.com/arnavdas88/drf-manager",
    },
    license='LICENSE',
    description='Django Rest Framework API Manager',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "pytest",

        # Django
        "django==4.0.6",

        # Django Rest Framework
        "pytz==2021.3",
        "djangorestframework==3.13.1",
    ],
    classifiers=[
        "Environment :: Web Environment",

        "Framework :: Django",

        "Intended Audience :: Developers",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",

        "Operating System :: OS Independent",

        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",

        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",

        "Topic :: Utilities"
    ],
    package_dir={ "": "src" },
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)