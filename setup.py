from setuptools import find_packages, setup

setup(
    name='metarchart',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'bokeh',
        'numpy',
        'requests',
        'metar',
        'flask_wtf',
        'wtforms',
    ],
)