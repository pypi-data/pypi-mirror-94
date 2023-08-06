from setuptools import setup

setup(
    name='abstractMLBaseModelTask',
    url='https://github.com/ulziiutas/abstractMLBaseModelTask',
    author='Ulzii-Utas Narantsatsralt',
    author_email='ulziiutas.n@gmail.com',
	setup_requires=['wheel'],
    packages=['abstractMLBaseModelTask'],
    # Needed for dependencies
    install_requires=['numpy', 'sklearn', 'seaborn', 'pandas', 'tensorflow'],
    version='0.2',
    license='MIT',
    description='Abstract Machine learning base model with analysis',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)