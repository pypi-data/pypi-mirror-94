from setuptools import find_packages
from distutils.core import setup
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(name='gbprocess-ngs',
      use_scm_version={'write_to': 'gbprocess/version.py'},
      long_description=long_description,
      long_description_content_type="text/markdown",
      setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
      extras_require={'docs': ['sphinx','sphinx_rtd_theme','sphinx-tabs']},
      description='GBprocesS allows for the extraction of genomic inserts from NGS data for GBS experiments',
      author='Dries Schaumont',
      author_email='dries.schaumont@ilvo.vlaanderen.be',
      install_requires=['BioPython>=1.78', 'cutadapt'],
      entry_points={
        'console_scripts': [
            'gbprocess = gbprocess.__main__:main',
            ],
        },
        packages = ['gbprocess','gbprocess.operations'],
      python_requires='>=3.7',
)
