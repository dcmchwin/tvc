from setuptools import setup

version = '0.0.0'

setup(name='tvc',
      version=version,
      tests_require=['pytest'],
      packages=[
          'tvc'
      ],
      entry_points={
          'console_scripts': [
              'tvc=tvc.main:main'
          ],
      }
      )
