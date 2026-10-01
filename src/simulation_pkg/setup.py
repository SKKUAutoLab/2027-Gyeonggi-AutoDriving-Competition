import os
from glob import glob
from setuptools import setup

package_name = 'simulation_pkg'
sub_package_name = 'simulation_pkg/lib'

setup(
    name=package_name,
    version='0.0.0',
    
    packages=[package_name, sub_package_name],
    
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name,'launch'), glob('launch/*')),
        (os.path.join('share', package_name,'worlds'), glob('worlds/*')),
        (os.path.join('share', package_name,'rviz'), glob('rviz/*')),
    ],
    
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Jinsun-Lee',
    maintainer_email='012vision@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'load_ego_car_node = simulation_pkg.lib.load_ego_car_node:main',
            'sim_simulation_sender_node = simulation_pkg.simulation_sender_node:main',
        ],
    },
)
