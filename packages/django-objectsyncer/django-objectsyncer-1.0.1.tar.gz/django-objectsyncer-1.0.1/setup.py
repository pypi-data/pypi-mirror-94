import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-objectsyncer", 
    version="1.0.1",
    author="mneitsabes",
    author_email="mneitsabes@nulloz.be",
    description="A Django ObjectSyncer between a server and multiples clients",
    long_description=long_description,
    long_description_content_type="text/markdown",
	keywords = ['django', 'object', 'sync'],
    url="https://github.com/mneitsabes/django-objectsyncer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	install_requires=[       
          'django',
          'django-model-utils',
          'requests',
          'djangorestframework',
      ],
    python_requires='>=3.6',
)