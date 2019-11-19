from setuptools import find_packages, setup


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="{{ project }}",
    version="0.0.0-beta.1",
    author="",
    author_email="",
    url="https://github.com/:username/{{ project }}",
    description="",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license="BSD",
    install_requires=[],
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    project_urls={
        "Documentation": "https://github.com/:username/{{ project }}/",
        "Source Code": "https://github.com/:username/{{ project }}/",
    },
    entry_points={
        'console_scripts': [
            '{{ project }}=app:main',
        ]
    },
    scripts=['app.py']
)
