from setuptools import setup


# This call to setup() does all the work
setup(
    name="razrda_binomial_options_pricing",
    version="1.0.2",
    author="Muhammad Raza",
    description='Binomial Options Pricing for European and Amrerican. Suitable for Visualizations.',
    packages=["razrda_binomialoptionspricing"],
    include_package_data=True,
    install_requires=["networkx",'matplotlib']
)
