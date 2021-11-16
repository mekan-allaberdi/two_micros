import setuptools

__version__ = '0.1'

config = {
    'name': 'two_micros',
    'author': 'Mekan ALLABERDIYEV <mekan.allaberdi@gmail.com>',
    'author_email': 'mekan.allaberdi@gmail.com',
    'version': __version__,
    'install_requires': [
                'sqlalchemy',
                'kafka-python',
                'pillow',
                'psycopg2'],
    'tests_require': ['nose'],
    'include_package_data': True,
    'zip_safe': False,
    'scripts': [],
    'entry_points': {
        'console_scripts': [
            'dls=two_micros.download_service:main',
            'cs=two_micros.concatenation_service:main'
        ]
    }
}

print('Places Version: %s' % __version__)

packages = setuptools.find_packages()
config['packages'] = packages
setuptools.setup(**config)
