from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Intended Audience :: Education',
]

setup(
    name = "Devil's Calculator",
    version = '0.0.1',
    description = 'Hail Hydra',
    long_description = open('README.txt').read() + '\n\n\n' + open('License.txt').read(),
    url = 'https://en.wikipedia.org/wiki/Kryptos',
    author = 'M3ph1st0',
    author_email = 'h3llsk1tch3n13@hell.com',
    license = 'MIT',
    classifiers = classifiers,
    keywords = ['add','sub','mul','div'],
    packages = find_packages(),
    install_requires = ['']

)