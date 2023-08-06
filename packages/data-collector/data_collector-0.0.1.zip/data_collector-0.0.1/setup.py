from setuptools import setup
import os


def strip_comments(line):
    return line.split('#', 1)[0].strip()


def reqs(*f):
    return list(filter(None, [strip_comments(ln) for ln in open(os.path.join(os.getcwd(), *f)).readlines()]))


setup(
    name='data_collector',
    version='0.0.1',
    description='package to load data to DW',
    author='Aare Laponin',
    author_email='aarelaponin@gmail.com',
    url='https://github.com/aarelaponin/data_collector.git',
    install_requires=reqs('requirements.txt'),
    package_dir={'': 'data_collector'},
    python_requires='>=3.9, <4',
    license='MIT',
)
