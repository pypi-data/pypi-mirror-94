import io
from setuptools import setup

def read_files(files):
    data = []
    for file in files:
        with io.open(file, encoding='utf-8') as f:
            data.append(f.read())
    return "\n".join(data)

long_description = read_files(['README.md'])

setup(name='snowconvert-test-utils',
      version='0.2',
      url='https://github.com/orellabac/snowconvert-test-utils',
      description="Adds some helper functions to make testing python modules easier",
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Mauricio Rojas',
      author_email='mauricio.rojas@mobilize.net',
      license='MIT',
      install_requires=[
        'snowflake-connector-python',
        'pytest',
        'python-dotenv'],
      packages=['testutils'],
      zip_safe=False)
