from distutils.core import setup

setup(name='argp',
      version='2.0.0',
      description='Minimal wrapper for initializing argparse',
      author='Ville M. Vainio',
      author_email='ville.vainio@basware.com',
      url='https://github.com/vivainio/argp',
      packages=['argp'],
      install_requires=[],
      package_data={
          "argp": ["py.typed"]
      }
      )
