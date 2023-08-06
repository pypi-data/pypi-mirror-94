from setuptools import setup, find_packages

setup(name="mess_server_leget",
      version="0.0.1",
      description="mess_server",
      author="Dmitriy Lobanov",
      author_email="lobanov.leget@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
