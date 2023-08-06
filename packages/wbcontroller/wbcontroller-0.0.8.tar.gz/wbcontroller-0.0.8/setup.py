from setuptools import setup

setup(
    name='wbcontroller',
    version='0.0.8',
    license='MIT License',
    author='Miguel L. Rodrigues',
    author_email='miguellukas52@gmail.com',
    keywords='webots basic python setup',
    description='Setup básico inicial para projetos utilizando o WeBots',
    packages=['wbcontroller'],
    package_data={'wbcontroller': ['_controller.so']},
    include_package_data=True,
    install_requires=[],
)