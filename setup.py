from setuptools import setup

version = '0.0.0'

setup(name='tvc',
      version=version,
      test_required=[],
      packages=[
          'tvc'
      ],
      entry_points={
          'console_scripts': [
              'tvc=tvc.main:main'
          ],
      }
      )
