from distutils.core import setup


setup(
    name="fqrweaveSDK",
    packages=["fqrweaveSDK"],
    version="0.1.5",
    description="SDK to interact with fQR Weave platform",
    url="https://github.com/fQR-Weave/python-sdk",
    author="wojak-frog",
    author_email="fqrweave@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",

    ],

    include_package_data=True,
    install_requires=[
        "arweave-python-client", "bs4", "qrcode", "pandas"
    ]
)