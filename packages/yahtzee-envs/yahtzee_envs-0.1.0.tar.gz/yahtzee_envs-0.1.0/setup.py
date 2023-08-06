from setuptools import setup


setup(name='yahtzee_envs',
      version='0.1.0',
      description='A growing collection (currently just 1) of environments for \
        training RL agents and experiementing with various RL methods and\
        algorithms.',
      long_description='',
      url='https://github.com/tomarbeiter/yahtzee-envs',
      author='Tom Arbeiter',
      license='Apache 2.0',
      packages=['yahtzee_envs'],
      install_requires=['sphinx', 'yahtzee-api'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        'Intended Audience :: Developers',
      ],
      )
