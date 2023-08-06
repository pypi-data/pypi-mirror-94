import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


python_version = '3.7'


setup(
    name='scipy-steadystate',
    version='0.1',
    author='Mischa Krüger',
    author_email="makmanx64@gmail.com",
    description='SciPy extension modules for general purpose steady-state solvers for differential state-equations.',
    keywords='numerics differential-equations ivp',
    url='https://gitlab.com/Makman2/scipy-steadystate',
    project_urls={
        'Bug Tracker': 'https://gitlab.com/Makman2/scipy-steadystate/issues',
        'Source Code': 'https://gitlab.com/Makman2/scipy-steadystate/-/tree/master',
    },
    platforms='any',
    license='MIT',
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',
    classifiers=[
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        f'Programming Language :: Python :: {python_version}',
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    packages=find_packages(),
    python_requires=f'>={python_version}',
    install_requires=read('requirements.txt').splitlines(),
    tests_require=read('test-requirements.txt').splitlines(),
    setup_requires=read('setup-requirements.txt').splitlines(),
)
