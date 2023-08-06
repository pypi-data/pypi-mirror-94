import setuptools
from pathlib import Path


README = (Path(__file__).parent/"README.md").read_text()

setuptools.setup(
    name="streamlit-data-profile-viewer",
    version="0.1.2",
    author="Sonia Castelo Quispe",
    author_email="",
    description="Data profile viewer component for Streamlit",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        "streamlit>=0.63",
        "data-profile-viewer>=0.2.6",
    ],
)
