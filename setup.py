import setuptools

setuptools.setup(
    name='fridgecamera',
    version='1.0.0',
    url='https://github.com/jacobolofsson/fridge_camera',
    author='Jacob Olofsson',
    author_email='jacob@jacobolofsson.se',
    description='I want to be able to check the content of my fridge online',
    packages=setuptools.find_packages(),
    install_requires=["opencv-python"],
    extras_require={"hardware_access": [
        "adafruit-circuitpython-ads1x15",
    ]},
    entry_points={"console_scripts": [
        "fridgecamera=fridgecamera.__main__:main",
    ]},
)
