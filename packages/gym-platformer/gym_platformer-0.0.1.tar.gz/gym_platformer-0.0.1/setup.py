from setuptools import setup, find_packages
setup(name='gym_platformer',
      packages=find_packages(),
      version='0.0.1',
      install_requires=['gym', 'numpy', 'pandas', 'joblib']
)