from bs4 import BeautifulSoup

from football import Drive
from football.scraper import get_page
from football.plays import StandardPlay


class PlayByPlay:
    _url_format = 'http://espn.go.com/nfl/playbyplay?gameId={game_id}'

    def __init__(self, game_id):
        """
        Get the box score page
        :param game_id: game_id
        """
        self._game_id = game_id
        url = self._url_format.format(game_id=game_id)
        self._soup = BeautifulSoup(get_page(url))

        self._home = self._soup.find('div', 'team home').find('span', 'abbrev').text
        self._away = self._soup.find('div', 'team away').find('span', 'abbrev').text

        try:
            self._home_score = int(self._soup.find('div', 'team home').find('div', 'score-container').text)
            self._away_score = int(self._soup.find('div', 'team away').find('div', 'score-container').text)
        except ValueError:
            # The game hasn't happened yet
            self._home_score = None
            self._away_score = None

    @property
    def home(self):
        return self._home

    @property
    def away(self):
        return self._away

    @property
    def home_score(self):
        return self._home_score

    @property
    def away_score(self):
        return self._away_score

    def get_drives(self):
        """
        Scrape the list of drives from this box score page
        :return: yields all Drives from this game
        """
        drive_items = self._soup.find_all('li', class_='accordion-item')
        for drive_html in filter(lambda x: 'half-time' not in x.attrs.get('class'), drive_items):
            yield Drive(drive_html)

    def get_play_data(self):
        """
        Get dicts for plays in this game
        :return: yields dicts for play-by-play data
        """
        final_lookup = {
                self.home: self.home_score,
                self.away: self.away_score
        }

        drives = list(self.get_drives())
        for i, drive in enumerate(drives):
            for play in drive.plays:
                if isinstance(play, StandardPlay):
                    previous_index = i - 1
                    if previous_index < 0:
                        offense_score = 0
                        defense_score = 0
                    else:
                        offense_score = drives[previous_index].get_score(drive.offense)
                        defense_score = drives[previous_index].get_score(drive.defense)

                    yield dict(down=play.down, distance=play.distance, field_position=play.field_position,
                               offense_score=offense_score, defense_score=defense_score,
                               time_left=(4 - play.quarter) * 15 * 60 + play.seconds,
                               drive_number=i, game_id=self._game_id, offense=drive.offense, defense=drive.defense,
                               offense_final=final_lookup[drive.offense], defense_final=final_lookup[drive.defense])
