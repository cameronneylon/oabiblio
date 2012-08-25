from setuptools import setup, find_packages

setup(
        author='Cameron Neylon',
        author_email=None,
        classifiers=[
            "Intended Audience :: Science/Research"
            ], # Fill these in from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        description="Report on open access journal numbers.",
        entry_points={
            'console_scripts' : [
                'oacensus = oabiblio.oacensus_commands:run'
                ]
            },
        include_package_data=True,
        install_requires=[
            'Markdown',
            'jinja2',
            'python-modargs>=1.4'
            ],
        name='oabiblio',
        packages=find_packages(),
        package_data = { "oabiblio" : ["data/*"] },
        url=None,
        version='0.0.1'
        )
