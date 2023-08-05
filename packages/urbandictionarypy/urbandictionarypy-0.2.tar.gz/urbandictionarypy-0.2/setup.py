from setuptools import setup
from setuptools import find_packages
setup(name='urbandictionarypy',
      version='0.2',
      description="A simple api wrapper for urban dictionary's api.",
      author='Jacks0n9',
      license='MIT',
      packages=find_packages("urbanpy"),
      zip_safe=False)