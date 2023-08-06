from setuptools import setup

setup(name='lifxdaycycle',
      version='0.112',
      description='changes brightness and light temperature based on the time of the day',
      url='https://github.com/slimneotech/lifxdaycycle',
      author='slimneotech',
      author_email='22907654+slimneotech@users.noreply.github.com',
      license='MIT',
      packages= ['lifxdaycycle'],
      # py_module=['lifxdaycycle', ],
      install_requires=[
           'lifxlan'
      ],
      entry_points={
          'console_scripts': [
                'light=lifxdaycycle.lightmanager:main',
          ],
      },
      zip_safe=False)