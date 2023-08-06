from setuptools import _install_setup_requires, setup,find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 8',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
]

setup(
    name = 'The Calculator',
    version = '0.0.1',
    description = 'Sort of guideleines.',
    Long_description = open('readme.txt').read() + '\n\n\n' + open('changelog.txt').read(),
    url = '',
    author = 'Eternal',
    author_email = 'eternal@gmail.com',
    license = 'MIT',
    classifiers = classifiers,
    keywords = ('add','sub','mul','div'),
    packages = find_packages(),
    install_requires = ['']
)