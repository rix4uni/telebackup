from setuptools import setup, find_packages

def dependencies(imported_file):
    """ __Doc__ Handles dependencies """
    with open(imported_file) as file:
        return file.read().splitlines()

setup(
    name="telebackup",
    packages=find_packages(),
    version=__import__("telebackup").__version__,
    description="Scrape all posts in a telegram channel and saves to another channel.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="rix4uni",
    url="https://github.com/rix4uni/telebackup",
    author_email="rix4uni@gmail.com",
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'telebackup=telebackup.telebackup:main',  # Adjust the import path for main
        ],
    },

    # install_requires=[],  # Add any dependencies if needed
    install_requires=dependencies('requirements.txt'),
)
