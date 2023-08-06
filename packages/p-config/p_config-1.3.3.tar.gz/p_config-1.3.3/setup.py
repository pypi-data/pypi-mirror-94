import setuptools

with open('README.rst') as f:
    long_description = f.read()

setuptools.setup(
    name='p_config',
    version='1.3.3',
    author='Abraham',
    author_email='abraham.liu@hotmail.com',
    description='small tool for project config management',
    install_requires=['PyYAML'],
    long_description=long_description,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
