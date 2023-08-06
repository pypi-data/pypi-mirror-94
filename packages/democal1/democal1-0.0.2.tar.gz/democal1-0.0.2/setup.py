from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
]


setup(
    name='democal1',
    version='0.0.2',
    description='dummycalci1',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='amrit250',
    author_email='amrit.gaur549@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='speedtest',
    packages=find_packages(),
    install_requires=['']
)
