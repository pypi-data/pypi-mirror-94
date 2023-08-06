from setuptools import setup

url = "https://github.com/jic-dtool/dtool-lookup-server-annotation-filter-plugin"  # NOQA
version = "0.2.0"
readme = open('README.rst').read()

setup(
    name="dtool-lookup-server-annotation-filter-plugin",
    packages=["dtool_lookup_server_annotation_filter_plugin"],
    description="Extend dtool-lookup-server with ability to filter by annotations",  # NOQA
    long_description=readme,
    install_requires=[
        "flask",
        "dtool-lookup-server>=0.15.0",
        "dtoolcore>=3.17.0",
    ],
    include_package_data=True,
    author="Tjelvar Olsson",
    author_email="tjelvar.olsson@gmail.com",
    version=version,
    url=url,
    entry_points={
        "dtool_lookup_server.blueprints": [
            "dtool_lookup_server_annotation_filter_plugin=dtool_lookup_server_annotation_filter_plugin:annotation_filter_bp",  # NOQA
        ],
    },
    download_url="{}/tarball/{}".format(url, version),
    license="MIT"
)
