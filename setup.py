from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='list_search',
    version='0.1.3',
    author='Dmitry Buslov',
    author_email='buslovdmitrij0@gmail.com',
    description='Search in list of dictionaries with lookups! Like in ORM!',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mrbuslov/list-search',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ],
    python_requires='>=3.9',
    install_requires=[],
)
