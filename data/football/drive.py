import re
from .play_parser import parse_play
from logger import logger


class Drive:
    def __init__(self, html):
        self._result = html.find('span', class_='headline').text

        self._offense, self._defense = self._parse_sides(html)

        minutes, seconds = html.find('span', class_='drive-details').text.split(',')[-1].split(':')
        self._seconds = 60 * int(minutes) + int(seconds)

        self._plays = self._parse_plays(html)

    @property
    def plays(self):
        return self._plays

    def _parse_plays(self, html):
        """
        Parses the plays for this drive
        :param html: html for the drive
        :return: yields the plays in the drive
        """
        for play in html.find_all('li'):
            header = play.find('h3').text
            text = play.find('p').text
            try:
                yield parse_play(header, text, self._offense)
            except Exception as e:
                logger.info("Error parsing: {header} {text} because {error}"
                            .format(header=header.strip(), text=text.strip(), error=e.message))

    @staticmethod
    def _parse_sides(html):
        """
        Find which team is on offense and which is on defense
        :param html: html for the drive
        :return: offensive team, defensive team
        """
        offense_name = str.upper(re.findall('nfl/500/[a-z]*\.png', html.find('img').get('src'))[0][8:-4])

        home_team = html.find('span', class_='home').find('span', class_='team-name').text
        away_team = html.find('span', class_='away').find('span', class_='team-name').text

        if home_team == offense_name:
            offense = home_team
            defense = away_team
        else:
            assert away_team == offense_name
            offense = away_team
            defense = home_team

        return offense, defense
