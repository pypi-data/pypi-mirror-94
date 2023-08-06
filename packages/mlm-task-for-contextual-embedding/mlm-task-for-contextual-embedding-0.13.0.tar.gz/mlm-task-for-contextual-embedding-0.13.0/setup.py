from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='mlm-task-for-contextual-embedding',
    packages=find_packages(),
    version='0.13.0',
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
        "packagename": [
            "log_config.ini"
        ]},
    include_package_data=True,
)
