from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'My second Python package'
LONG_DESCRIPTION = 'My second Python package that can sum and multiply two numbers'

# Setting up
setup(
       # the name must match the folder name 'plk_package'
        name="plk_package22",
        version=VERSION,
        author="Philip Luke K ",
        author_email="philip_luke@ce.iitr.ac.in",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ]
)
