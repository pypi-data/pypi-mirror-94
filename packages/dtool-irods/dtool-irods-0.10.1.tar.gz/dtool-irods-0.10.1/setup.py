from setuptools import setup

url = "https://github.com/jic-dtool/dtool-irods"
version = "0.10.1"
readme = open('README.rst').read()

setup(
    name="dtool-irods",
    packages=["dtool_irods"],
    version=version,
    description="Add iRODS support to dtool",
    long_description=readme,
    include_package_data=True,
    author="Tjelvar Olsson",
    author_email="tjelvar.olsson@jic.ac.uk",
    url=url,
    download_url="{}/tarball/{}".format(url, version),
    install_requires=[
        "click",
        "dtoolcore>=3.17",
    ],
    entry_points={
        "dtool.storage_brokers": [
            "IrodsStorageBroker=dtool_irods.storagebroker:IrodsStorageBroker",
        ],
    },
    license="MIT"
)
