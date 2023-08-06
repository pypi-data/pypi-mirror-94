from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='Aman Calculator Pycharm',
    version='0.0.1',
    description='Our package has basic calculator function such as addition, subtraction, multiplication and division.',
    long_description=open('README.txt').read() + '\n\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Aman Singh',
    author_email='r.amansingh241201@gmail.com',
    license="MIT",
    classifiers= classifiers,
    keywords=('add', 'sub','mul','div'),
    packages=find_packages(),
    install_require=['']
)

# pip3 install setuptools twine
# go to our folder
# python setup.py sdist
# twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
# twine upload -u AmanPycharm12 -p #$WcT?79?w+r#ip --repository-url https://upload.pypi.org/legacy/ dist/*

