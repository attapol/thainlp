from setuptools import setup

setup(name='thainlp',
      version='0.1',
      description='Thai Natural Language Processing Tools',
      author='Attapol Rutherford',
      author_email='attapolrutherford@gmail.com',
      license='MIT',
      packages=['thainlp', 'thainlp.tokenization'],
      install_requires=['sklearn_crfsuite'],
      package_data={'thainlp.tokenization': 'crf*'},
      install_package_data=True,
      test_suite='thainlp.tests'
      )
