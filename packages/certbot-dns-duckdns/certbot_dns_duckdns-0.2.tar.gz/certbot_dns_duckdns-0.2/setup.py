from setuptools import setup, find_packages

import certbot_dns_duckdns

with open("Readme.md") as f:
    long_description = f.read()

setup(
    name="certbot_dns_duckdns",
    version=certbot_dns_duckdns.__version__,
    author="infinityofspace",
    url="https://github.com/infinityofspace/certbot_dns_duckdns",
    description="Obtain certificates using a DNS TXT record for DuckDNS domains",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Utilities",
        "Topic :: System :: Systems Administration"
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "setuptools",
        "zope.interface",
        "certbot",
        "requests"
    ],
    entry_points={
        "certbot.plugins": [
            "dns-duckdns = certbot_dns_duckdns.cert.client:Authenticator",
        ]
    }
)
