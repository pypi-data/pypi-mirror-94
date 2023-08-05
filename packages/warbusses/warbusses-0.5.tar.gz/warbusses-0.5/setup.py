import setuptools

with open('readme.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='warbusses',
    version='0.5',
    description='Useful info about warsaw busses',
    long_description=long_description,
    packages=['warbusses'],
    classifiers=[
        'Programming Language :: Python :: 3'
    ],
    url='https://github.com/szczor/warbusses'

)
