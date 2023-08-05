import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='trading-bot-predictor',
    version='0.0.1',
    author='asconius',
    description='Timeseries forecasting for stock prediction',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Asconius/predictor',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
