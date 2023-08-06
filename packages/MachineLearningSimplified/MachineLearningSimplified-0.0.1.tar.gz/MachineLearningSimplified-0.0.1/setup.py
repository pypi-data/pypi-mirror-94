from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'Machine Learning Simplified'
LONG_DESCRIPTION = 'A package that simplifies machine learning for you!'

# Setting up
setup(
    name="MachineLearningSimplified",
    version=VERSION,
    author="Taptaplit10",
    author_email="<no-reply@taptaplit.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib', 'random', 'pandas'],
    keywords=['machine-learning', 'ml', 'linear-regression', 'K-nearest-neighbors'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)