from setuptools import setup, find_packages

with open('requirements.txt', 'r') as requirements:
    setup(
        name='datalib-dev',
        version='0.0.1',
        install_requires=list(requirements.read().splitlines()),
        packages=find_packages(),
        description=
            'library for loading, processing, and splitting common datasets',
        python_requires='>=3.6',
        author='Klas Leino',
        long_description='file: README.md',
        long_description_content_type='text/markdown'
    )
