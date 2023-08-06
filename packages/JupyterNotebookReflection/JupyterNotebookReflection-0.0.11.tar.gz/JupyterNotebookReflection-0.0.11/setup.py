from setuptools import setup, find_packages


from os import path
this_directory = path.abspath(path.dirname(__file__))
readme = open(path.join(this_directory, 'README.md')).read()
changelog = open(path.join(this_directory, 'CHANGELOG.md')).read()


setup(
    name='JupyterNotebookReflection',
    version='0.0.11',
    description='A module to perform reflection coding in Jupyter notebooks.',
    long_description=(readme + '\n\n' + changelog),
    long_description_content_type='text/markdown',
    url='',
    author='Charles Varley',
    license='MIT',
    keywords=['jupyter','notebook','reflection','introspection'],
    packages=['JupyterNotebookReflection'],
    package_data={'JupyterNotebookReflection': ['*.js']},
)