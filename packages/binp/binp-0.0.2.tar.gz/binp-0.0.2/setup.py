from os import getenv

import setuptools

version = getenv('GITHUB_REF', getenv('VERSION', 'dev')).split('/')[-1].strip('v')

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name="binp",
                 version=version,
                 author="Aleksandr Baryshnikov",
                 author_email="owner@reddec.net",
                 description="Basic Integration Platform",
                 license='MIT',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 include_package_data=True,
                 package_data={
                     'binp': ['migrations', 'static']
                 },
                 url="https://github.com/reddec/binp",
                 packages=['binp'],
                 classifiers=[
                     "Programming Language :: Python :: 3.8",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                     "Intended Audience :: Developers",
                     "Intended Audience :: System Administrators"
                 ],
                 python_requires='>=3.8',
                 install_requires=[
                     'fastapi~=0.63.0',
                     'aiofiles~=0.6.0',
                     'databases[sqlite]~=0.4.1'
                 ])
