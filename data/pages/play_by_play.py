from bs4 import BeautifulSoup
from scraper import get_page
from football import Drive


class PlayByPlay:
    _url_format = 'http://espn.go.com/nfl/playbyplay?gameId={game_id}'

    def __init__(self, game_id):
        """
        Get the box score page
        :param game_id: game_id
        """
        url = self._url_format.format(game_id=game_id)
        self._soup = BeautifulSoup(get_page(url))

    def get_drives(self):
        """
        Scrape the list of drives from this box score page
        :return: yields all Drives from this game
        """
        drive_items = self._soup.find_all('li', class_='accordion-item')
        for drive_html in filter(lambda x: 'half-time' not in x.attrs.get('class'), drive_items):
            yield Drive(drive_html)