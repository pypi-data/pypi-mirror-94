from setuptools import setup, find_packages

setup(name='slack_integration',
      version='0.0.4',
      description='The funniest joke in the world',
      long_description='Really, the funniest around.',
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='funniest joke comedy flying circus',
      url='https://github.com/GhostNA/slack-integration',
      author='Specter NA',
      author_email='naspecter@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'markdown',
      ],
      include_package_data=True,
      zip_safe=False)
