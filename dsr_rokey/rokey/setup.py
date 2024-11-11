from setuptools import find_packages, setup

package_name = 'rokey'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='juwan',
    maintainer_email='dlacksdn352@gmail.com',
    description='ROKEY BOOT CAMP Package',
    license='Apache 2.0 License',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "force_control = rokey.basic.force_control:main",
            "pick_and_place = rokey.basic.pick_and_place:main",
            "sorting = rokey.basic.sorting:main",
            "cup_stack= rokey.basic.stacking:main",
            "tool_force = rokey.state_publisher.tool_force:main",
            "posj_publisher = rokey.state_publisher.posj_publisher:main"
        ],
    },
)
