from setuptools import setup, find_packages

setup(
    name='project0',
    version='1.0',
    author='Varshitha Choudary Vasireddy',
    author_email='varshitha.c.vasireddy@ou.edu',
    packages=find_packages(exclude=('tests', 'docs')),
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)
