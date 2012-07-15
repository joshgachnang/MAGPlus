from distutils.core import setup

setup(
    name='MAGPlus',
    version='0.1.1',
    author='Josh Gachnang',
    author_email='Josh@ServerCobra.com',
    packages=['magplus',],
    url='http://pypi.python.org/pypi/MAGPlus/',
    license='GPLv2',
    description='Retrieving latest Minecraft versions.',
    long_description=open('README.rst').read(),
    install_requires=[
    'beautifulsoup4 >= 4.1.1',
    ]
)
