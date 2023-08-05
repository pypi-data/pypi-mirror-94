from setuptools import setup

with open('README.md', 'r') as f:
    README = f.read()

setup(
    name='iotanalyzer',
    version='0.0.1',
    description='IoTAnalyzer is an open-source IoT device management toolkit that can help smart home owner, Internet Service Providers (ISPs), and researchers to automatically monitor smart home IoT devices, and analyze potential security and privacy vulnerabilities.',
    
    long_description=README,
    long_description_content_type="text/markdown",
    
    url='https://github.com/gghg1989/IoTAnalyzer',

    author='Aaron Feng',
    author_email='gghg1989@gmail.com',

    py_modules=['iotanalyzer'],
    package_dir={'': 'src'},

    install_requires=[
        'pandas==1.1.2',
        'numpy==1.19.2',
        'scikit-learn==0.23.2',
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ]
)