import setuptools

with open("README_pypi.md", "r") as fh:
    long_description = fh.read()


def _parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


requirements = _parse_requirements('requirements.txt')

proj_classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: Apache Software License',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: Implementation',
    'Topic :: Database',
    'Topic :: Software Development :: Code Generators',
    'Topic :: Utilities',
]

setuptools.setup(
    name="hashmap-data-definitionOps",
    version="0.0.0.28",
    author="Hashmap, Inc",
    author_email="accelerators@hashmapinc.com",
    description="An alternative approach utility for data warehouse DevOps for Snowflake - limited usage.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/hashmapinc/oss/dwmetareplicate_snowflake",
    packages=setuptools.find_packages(),
    package_data={
        "hmddops_resources.config": ['*.yaml'],
        'hmddops_resources.templates': ['*.sql']
    },
    include_package_data=True,
    classifiers=proj_classifiers,
    entry_points={
        'console_scripts': ['hmddops=hm_datadefinitionops.__main__:main'],
    },
    install_requires=requirements,
    python_requires='>=3.6',
)
