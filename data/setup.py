from distutils.core import setup

setup(
        name='football',
        version='0.1',
        packages=['football', 'football.plays', 'football.pages'],
        url='https://github.com/NathanDeMaria/Football/tree/master/data',
        license='',
        author='Nathan DeMaria',
        author_email='nathandmaria@gmail.com',
        description='Python package for collecting NFL play-by-play data from ESPN.com'
)
