from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

print(find_packages())
setup(
    name='mlm-task-for-contextual-embedding',
    packages=find_packages(),
    version='0.18.0',
    description='a machine learning project for mlm task for contextual embedding',
    author='Simon Meoni',
    license='MIT',
    install_requires=requirements,
    entry_points='''
    [console_scripts]
    camembert_mlm_ft=src.models.camembert_mlm_ft:main
    make_dataset=src.data.make_dataset:main
    ''',
    package_data={
        find_packages()[0]: [
            "log_config.ini"
        ]},
)
