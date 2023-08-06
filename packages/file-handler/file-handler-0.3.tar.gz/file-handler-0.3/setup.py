from setuptools import setup,find_packages

def read_requirements():
    with open('requirements.txt','rb') as req:
        rlist=req.read().decode('utf-16').split('\n')
    return rlist

setup(
    name='file-handler',
    version='0.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points={'console_scripts':
['fim=fim.cli:main'],},
        )