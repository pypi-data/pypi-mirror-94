import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='flask-add-ons',
    version=0.1,
    author='David Meyer',
    author_email='dameyerdave@gmail.com',
    description='Flask add ons',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.5',
    url='https://github.com/dameyerdave/flask-add-ons',
    packages=setuptools.find_packages(exclude='test'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    install_requires=[
      'blessings'
    ]
)
