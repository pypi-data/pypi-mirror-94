from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='dockit',
    version='0.1.6',  # pypi
    # version='0.0.5',  # pypi_test
    author='Ron Chang',
    author_email='ron.hsien.chang@gmail.com',
    description=(
        'Fuzzy the current location to pull all the submodules '
        'and specify the project if required. '
        'To launch, close and execute container with docker-compose '
        'and its relative services without change the directory.'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Ron-Chang/dockit.git',
    packages=find_packages(),
    license='MIT',
    python_requires='>=3.6',
    exclude_package_date={'':['.gitignore', 'asset', 'test', 'setup.py']},
    scripts=['bin/dockit'],
)
