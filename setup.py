from setuptools import setup

setup(
    name='crash_reporter',
    version='0.1.0',
    author='The Servo Project Developers',
    url='https://github.com/servo/crash-reporter',
    description='A service that collects Servo crash reports',

    packages=['crash_reporter'],
    install_requires=[
        'flask',
        'Flask-HTTPAuth',
    ],
    entry_points={
        'console_scripts': [
            'crash_reporter=crash_reporter.flask_server:main',
        ],
    },
    zip_safe=False,
)
