from setuptools import setup, find_packages

setup(
    name='pyflux-influxdb',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[
        "influxdb-client==1.13.0"
    ],
    include_package_data=True,
    url='https://broadtech.com.cn',
    license='GNU General Public License v3.0',
    author='Lee',
    author_email='canyun@live.com',
    description='influxdb pyflux',
)
