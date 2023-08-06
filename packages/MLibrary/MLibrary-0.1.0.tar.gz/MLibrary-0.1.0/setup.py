from setuptools import find_packages, setup

setup(
    name='MLibrary',
    packages=find_packages(include=['MLibrary']),
    version='0.1.0',
    description='Machine Learning Python Library',
    author='Alhuin',
    license='MIT',
    install_requires=['numpy'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
