import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tworavens_preprocess",
    version="1.1.5",
    author="Two Ravens Team",
    author_email="raman_prasad@harvard.edu",
    description="TwoRavens Preprocess package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TwoRavens/raven-metadata-service",

    packages=['raven_preprocess',
              'raven_preprocess.basic_utils'
              ],

    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # These classifiers are *not* checked by 'pip install'. See instead
        # 'python_requires' below.
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
        ],

        keywords='tworavens preprocess metadata',  # Optional

        python_requires='>=3.6',

        install_requires=[
            'pandas>=0.22.0',
            'scipy>=1.4.1',
            'simplejson>=3.13.2',
            'dictdiffer==0.8.1',
            'requests>=2.20.0',
            'numpy>=1.18.2',
            'xlrd>=1.1.0',
            'jsonschema>=2.6.0',
            'pycountry==19.8.18',
            'us==1.0.0'
        ],
)
