
from setuptools import setup, find_packages

from version_file_seeker import find_version

with open('README.md') as readme_file:
    readme = readme_file.read()


try:
    with open('HISTORY.rst') as history_file:

        history = history_file.read()
except BaseException:
    history = None


try:
    with open('Description.txt') as description_file:

        description = description_file.read()

except BaseException:
    description = None


try:
    with open('docs/requirements.txt') as requirements_file:
        read_lines = requirements_file.readlines()
        requirements = [line.rstrip('\n') for line in read_lines]

except BaseException:
    requirements = None


Version = find_version('', '__init__.py')


setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]


setup(name='IOP_AOPs',
      author="Philipe Riskalla Leal",
      author_email='leal.philipe@gmail.com',

      maintainer="Philipe Riskalla leal: developer",
      maintainer_email='leal.philipe@gmail.com',

      classifiers=[
          'Topic :: Education',  # this line follows the options given by: [1]
          # this line follows the options given by: [1]
          "Topic :: Scientific/Engineering",
          'Intended Audience :: Education',
          "Intended Audience :: Science/Research",
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ],

      keywords="fancy spatial plot, geopanda, xarray, matplotlib",

      description='This is a python package containing several algorithms for  \
                 acquisition of Optical Properties of water bodies by means \
                 of remote sensing data',

      long_description=description,

      license="MIT license",

      version=Version,

      # Requirements

      install_requires=requirements,
      setup_requires=setup_requirements,

      python_requires='>=3.7',  # Your supported Python ranges

      packages=find_packages(include='IOP_AOPs'),

      package_dir={'': 'IOP_AOPs'},

      # TODO: add example data
      # include_package_data=True,
      # package_data={'IOP_AOPs/tests/Data_example':
      # ['Data_example/MUNICIPIOS*']},

      # Testers:

      test_suite='nose.collector',
      tests_require=['nose'],

      url='https://github.com/PhilipeRLeal/IOP_AOPs.git',

      # download_url='TODO',

      zip_safe=False,
      )
