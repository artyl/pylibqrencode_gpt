from setuptools import setup

setup(
    name="pylibqrencode",
    version="0.1",
    packages=["pylibqrencode"],
    include_package_data=True,
    package_data={"pylibqrencode": ["qrpng.dll"]},
    install_requires=["Pillow"],
)
