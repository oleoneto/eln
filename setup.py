from setuptools import find_packages, setup


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="eln",
    version="0.0.0-beta.1",
    author="Leo Neto",
    author_email="apps@lehvitus.com",
    url="https://github.com/lehvitus/eln",
    description="A command-line tool for quick access to web services",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="cli command line tools miscellaneous news weather digitalocean s3 aws",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license="BSD",
    install_requires=[
        'Click==7.0',
        'requests',
        'pyttsx3',
        'jinja2',
        'inflection',
        'tox'
    ],
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    project_urls={
        "Documentation": "https://github.com/lehvitus/eln/",
        "Source Code": "https://github.com/lehvitus/eln/",
    },
    entry_points={
        'console_scripts': [
            'eln=app:main',
        ]
    },
    scripts=['app.py']
)