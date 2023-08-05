from setuptools import setup, find_packages

setup(name="client_app",
      version="0.0.2",
      description="client_app",
      author="Aleksey Ostryakov",
      author_email="test@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )