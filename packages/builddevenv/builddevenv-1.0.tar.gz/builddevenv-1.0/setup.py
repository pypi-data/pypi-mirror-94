from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='builddevenv',                    # package name
    version='1.0',                          # version
    description='Module that makes, in a development context, the creation of dockers containers easier.',      # short description
    author='Damien JADEAU',
    keywords = 'docker development deploy',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers = ['Topic :: Education', 'Topic :: Documentation', 'Development Status :: 5 - Production/Stable', 'Intended Audience :: Developers', 'Topic :: Software Development :: Build Tools'],
    license = 'GPL V3',
    url = 'https://github.com/djadeau-dvc/BuildDevEnv',               # package URL
    install_requires = [
        'docker==4.4.1',
        'PyYAML==5.4.1',
    ],                    # list of packages this package depends
    python_requires='>=3.6',
                                            # on.
    #packages=['builddevenv'],              # List of module names that installing
                                            # this package will provide.
)