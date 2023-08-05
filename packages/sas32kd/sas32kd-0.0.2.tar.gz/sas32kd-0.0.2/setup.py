from setuptools import setup


def readme_file_contents():
    with open('README.rst') as readme:
        data = readme.read()
    return data


setup(
    name='sas32kd',
    version='0.0.2',
    description='SAS 32KD USI Protocol Library',
    long_description=readme_file_contents(),
    author='avc',
    author_email='avcsec@protonmail.com',
    license='MIT',
    packages=['sas32kd'],
    zip_safe=False,
    install_requires=[]
)
