from setuptools import find_packages, setup

setup(
    packages=find_packages(include=['MLibrary']),
    install_requires=['numpy'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
