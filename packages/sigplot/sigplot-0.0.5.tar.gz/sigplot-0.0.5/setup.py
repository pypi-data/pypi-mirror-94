import setuptools
setuptools.setup(
  name='sigplot',
  packages=['sigplot'],
  version='0.0.5',
  license='MIT',
  description='Graphical library for signal processing',
  author='Hari',
  author_email='harikalyanraman@gmail.com',
  keywords=['signals', 'systems', 'convolution', 'fourier'],
  install_requires=[
          'numpy',
          'tk',
          'matplotlib'
      ],
  classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',
  ],
)

#python setup.py sdist bdist_wheel
#twine upload dist/*
