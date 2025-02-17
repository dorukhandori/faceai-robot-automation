from setuptools import setup, find_packages

setup(
    name='faceai_test',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'robotframework',
        'Appium-Python-Client',
        'PyYAML'
    ],
) 