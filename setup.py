import setuptools,os

print os.path.dirname(os.path.realpath(__file__))
#install_require = [line.strip() for line in 
#                 open('requirements.txt')
#                 if line.strip() and not line.strip().startswith('--')]

setuptools.setup(
    name='Voyage',
      version='0.0.1',
      description='Dashboard',
      author='Nishant Garg',
    #install_require=install_require,
    )