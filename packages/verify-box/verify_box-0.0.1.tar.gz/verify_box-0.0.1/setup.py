from setuptools import setup

setup(name='verify_box',
      version='0.0.1',
      description='Calculate accuracy between boxes in a image',
      url='https://github.com/thaithien001/verify_box',
      author='Thien Ng',
      author_email='thien.nguyenthai.ncc@gmail.com',
      license='MIT',
      packages=['accuracy'],
      install_requires=['numpy'],
      python_requires='~=3.3',
      zip_safe=False)
