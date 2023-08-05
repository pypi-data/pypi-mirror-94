from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='mlm-task-for-contextual-embedding',
    packages=find_packages(),
    version='0.1.0',
    description='a machine learning project for mlm task for contextual embedding',
    author='Simon Meoni',
    license='MIT',
    install_requires=requirements,
    entry_points='''
    [console_scripts]
    bert_mlm_ft=src.models.bert_mlm_ft:main
    ''',
)
