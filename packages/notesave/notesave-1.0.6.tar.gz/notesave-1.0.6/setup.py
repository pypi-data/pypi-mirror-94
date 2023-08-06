from distutils.core import setup
setup(
  name = 'notesave',
  author_email = 'example@example.com',
  version = '1.0.6',
  classifiers = [
      "Programming Language :: Python :: 3",
  ],
  description = ' A CLI for saving note locally and online',
  licence = 'MIT',
  instal_requires =['requests'],
  packages = ['notesave'],
  author = 'ninjamar',
  python_require = '>=3.6',
  entry_points = {
    'console_scripts':
    ['notesave=notesave.cli:main']
  },
  url = 'https://github.com/ninjamar/NoteSave'
)