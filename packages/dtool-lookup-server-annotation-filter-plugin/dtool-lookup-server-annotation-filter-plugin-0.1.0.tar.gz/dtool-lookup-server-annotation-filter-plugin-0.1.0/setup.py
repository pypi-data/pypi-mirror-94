from setuptools import setup

url = "https://github.com/jic-dtool/dtool-lookup-server-annotation-filter-plugin"  # NOQA
version = "0.1.0"
readme = open('README.rst').read()

setup(
    name="dtool-lookup-server-annotation-filter-plugin",
    description="Extend dtool-lookup-server with ability to filter by annotations",  # NOQA
    packages=["dtool_lookup_server_annotation_filter_plugin"],
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
