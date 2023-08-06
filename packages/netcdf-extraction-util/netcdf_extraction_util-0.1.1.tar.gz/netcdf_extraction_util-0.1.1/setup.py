from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()


setup(name="netcdf_extraction_util", version="0.1.1", 
      description="Script to extract time-series from Netcdf",
      long_description=readme(),
      long_description_content_type='text/x-rst',
      author="Daniel Lagrava",
      author_email="daniel.lagravasandoval@niwa.co.nz",
      url="https://github.com/daniel-lagrava-niwa/netcdf_extraction_util",
      license="GNU",
      packages=["netcdf_extraction_util"],
      entry_points={
        'console_scripts': [
            'netcdf_extraction_util=netcdf_extraction_util.command_line:main'
        ],
      },
      install_requires=['numpy','netCDF4','xarray'],
      include_package_data=True,
      zip_safe=False
)

