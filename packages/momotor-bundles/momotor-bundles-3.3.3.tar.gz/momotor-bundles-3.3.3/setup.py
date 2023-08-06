from setuptools import setup, find_namespace_packages


def get_version():
    import os.path

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, 'src/momotor/bundles/version.py'), 'r') as version_file:
        loc = {}
        exec(version_file.readline(), {}, loc)
        return loc['__VERSION__']


def get_long_description():
    with open("README.md", "r") as fh:
        return fh.read()


setup(
    name='momotor-bundles',
    version=get_version(),
    author='Erik Scheffers',
    author_email='e.t.j.scheffers@tue.nl',
    description="Momotor bundle reader, writer, tools",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url='https://momotor.org/',
    project_urls={
        'Documentation': 'https://momotor.org/doc/engine/momotor-bundles/',
        'Source': 'https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/',
        'Tracker': 'https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/issues',
    },
    install_requires=[
        'xsdata==21.1.*',
        'typing-extensions; python_version<"3.8"',
    ],
    python_requires='>=3.7',
    extras_require={
        'test': [
            'pytest',
            'pytest-cov',
            'pytest-pythonpath',
            'xmljson',
            'lxml',
        ],
        'docs': [
            'Sphinx',
            'sphinx-autodoc-typehints',
        ],
        'lxml': [
            'lxml',
        ]
    },
    packages=find_namespace_packages(where='src', include=('momotor.*',)),
    package_dir={'': 'src'},
    package_data={'': ['*.xsd']},
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    ],
)
