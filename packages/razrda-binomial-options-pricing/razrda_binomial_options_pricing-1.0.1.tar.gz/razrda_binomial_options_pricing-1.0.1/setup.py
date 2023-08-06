from setuptools import setup

# This call to setup() does all the work
setup(
    name="razrda_binomial_options_pricing",
    version="1.0.1",
    author="Muhammad Raza",
    packages=["razrda_binomialoptionspricing"],
    include_package_data=True,
    install_requires=["networkx",'matplotlib']
)
