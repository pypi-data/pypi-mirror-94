from setuptools import find_packages, setup

setup(
    name='adftestpy',
    packages=find_packages(include=['adftestpy']),
    version='0.3.0',
    description='Python library for running unit tests of Azure Data Factory configurations.',
    author='Ryan Brown',
    author_email='ryanbrownnetworking777@gmail.com',
    license='MIT',
    install_requires=['pytest-runner', 'azure-identity', 'azure-mgmt-datafactory', ],
    setup_requires=['pytest-runner', 'azure-identity', 'azure-mgmt-datafactory', ],
    tests_require=['pytest'],
    test_suite='tests',
)