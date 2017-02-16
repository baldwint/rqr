from setuptools import setup

# http://stackoverflow.com/a/7071358/735926
import re
VERSIONFILE='rqr/__init__.py'
verstrline = open(VERSIONFILE, 'rt').read()
VSRE = r'^__version__\s+=\s+[\'"]([^\'"]+)[\'"]'
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % VERSIONFILE)

with open('README.rst') as f:
    readme = f.read()

setup(name='rqr',
      version=verstr,
      description='A utility to render responses to '
                  'reading questions asked via Moodle.',
      long_description=readme,
      url='https://github.com/baldwint/rqr',
      author='Tom Baldwin',
      author_email='baldwint@lanecc.edu',
      license='MIT',
      classifiers=(
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Education',
          'Topic :: Utilities',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ),
      install_requires=['lxml'],
      packages=['rqr'],
      package_data={
          'rqr': ['templates/*.html'],
      },
      entry_points = {
          'console_scripts': ['rqr=rqr.__main__:main'],
      },
      )
