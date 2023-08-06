from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name='notifique-me',
    version='0.0.2',
    url='https://notifique-me.com',
    license='MIT License',
    author='Marcos Rafael Rodrigues',
	long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author_email='rafaeljacuri@gmail.com',
    keywords='Pacote',
    description=u'Pacote para enviar mensagem no WhatsApp e SMS, de graça para desenvolvedores',
    packages=['notifique-me'],
    install_requires=['http.client', 'json','print_function','SimpleNamespace','Namespace'],
)