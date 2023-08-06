from setuptools import setup

with open ('README','r') as fh:
    long_description = fh.read()

with open ('requirements.txt', 'r') as fh:
    required = fh.read().splitlines()

setup(
    name='EpinanoPredict',
    version='0.1.2',
    url='https://github.com/enovoa/EpiNano',
    author='Huanle Liu && Eva Novoa',
    author_email='huanle.liu@crg.eu',
    description='Predict m6A RNA modifications and train models using SVM',
    py_modules=["EpinanoPredict"],
    package_dir = {'': 'src'},
    classifiers = [
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent", 
    ],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    install_requires=required
)
