from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README
setup(
      name='evpy',
      version='1.0.4',
      description='A phython package to predict the efficiency/size of electronic powertrain components',
      long_description=readme(),
      long_description_content_type='text/markdown',
      author='Dalton Chancellor',
      license='MIT',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          ],
      packages=["evpy_"],
      include_package_data=True,
      install_requires=['scipy','numpy'],
      entry_points={
          'console_scripts': [
                'GUI3=GUI3.py']})
