from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='Anshu-Python-Calculator',
    version='0.0.1',
    description='Our package will give u a basic calculator function such as add, sub, mul, div',
    Long_description=open('README.txt').read() +
    '\n\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Anshu Bhagat',
    author_email='anshubahgat201@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=('add', 'sub', 'mul', 'div'),
    packages=find_packages(),
    install_require=['']

)
