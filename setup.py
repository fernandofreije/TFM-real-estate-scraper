# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name='project',
    version='1.0',
    packages=find_packages(),
    package_data={
        'real_estate_scraper': ['resources/*.yml']
    },
    entry_points={'scrapy': ['settings = real_estate_scraper.settings']},
)
