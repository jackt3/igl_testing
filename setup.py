from setuptools import setup, find_packages

setup(
    name='testing_igl',
    version='0.0.1',
    description='Quick demo for the libigl Python bindings',
    packages=find_packages(),
    install_requires=[
        'igl',
        'meshplot',
        'numpy',
        'nibabel',
        'scipy'
    ],
    entry_points={
        'console_scripts':
        [
            'lap_of_func = scripts.laplacian:main'
        ]
    }
)