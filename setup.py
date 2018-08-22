from setuptools import setup

try:
    with open('LICENSE.txt', 'r') as f:
        _license = f.read()
except:
    _license = ''

try:
    with open('README.rst', 'r') as f:
        _readme = f.read()
except:
    _readme = ''

setup(
  name='hlint',
  packages=['hlint'],
  version='0.0.1',
  description='HTML 5 Linter using Mozilla validation services',
  author='AndrewRPorter',
  author_email='porter.r.andrew@gmail.com',
  license=_license,
  long_description=_readme,
  url='https://github.com/AndrewRPorter/hlint',
  download_url='https://github.com/AndrewRPorter/hlint/releases',
  install_requires=['setuptools'],
)
