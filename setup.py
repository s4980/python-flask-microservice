from setuptools import setup

setup(
    name='svc-yammer',
    packages=['svc-yammer'],
    include_package_data=True,
    install_requires=[
        'flask',
        'cassandra-driver',
        'prometheus',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
