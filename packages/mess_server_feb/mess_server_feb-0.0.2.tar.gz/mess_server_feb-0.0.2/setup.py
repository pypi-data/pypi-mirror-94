from setuptools import setup, find_packages

setup(name="mess_server_feb",
      version="0.0.2",
      description="mess_server_feb",
      author="Ivan Ivanov",
      author_email="iv.iv@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
