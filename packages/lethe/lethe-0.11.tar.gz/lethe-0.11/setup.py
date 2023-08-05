#!/usr/bin/env python3

from setuptools import setup, find_packages


with open('README.md', 'rt') as f:
    long_description = f.read()

with open('lethe/VERSION.py', 'rt') as f:
    version = f.readlines()[2].strip()


setup(name='lethe',
      version=version,
      description='Git-based snapshotting',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Jan Petykiewicz',
      author_email='anewusername@gmail.com',
      url='https://mpxd.net/code/jan/lethe',
      packages=find_packages(),
      package_data={
          'lethe': ['py.typed'],
      },
      entry_points={
          'console_scripts': [
              'lethe=lethe:endpoints.main',
              'lethe-push=lethe:endpoints.push',
              'lethe-fetch=lethe:endpoints.fetch',
          ],
      },
      install_requires=[
            'typing',
      ],
      keywords=[
            'git',
            'snapshot',
            'commit',
            'refs',
            'backup',
            'undo',
            'log',
            'lab notebook',
            'traceability',
      ],
      classifiers=[
            'Programming Language :: Python :: 3',
            'Development Status :: 4 - Beta',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Topic :: Software Development :: Version Control :: Git',
            'Topic :: Utilities',
      ],
      )
