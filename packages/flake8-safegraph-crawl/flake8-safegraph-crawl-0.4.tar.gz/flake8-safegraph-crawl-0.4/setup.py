from setuptools import setup

package = "flake8-safegraph-crawl"
version = "0.4"

setup(
    name=package,
    version=version,
    description="Flake8 plugin enforcing code requirements for SafeGraph crawlers",
    url="https://github.com/SafeGraphInc/flake8-safegraph-crawl",
    packages=["flake8_safegraph_crawl"],
    entry_points={"flake8.extension": ["SG = flake8_safegraph_crawl:Plugin"]},
    setup_requires=["flake8", "pytest-runner"],
    tests_require=["pytest"],
)
