import re
from .play_parser import parse_play
from logger import logger


class Drive:
    def __init__(self, html):
        self._result = html.find('span', class_='headline').text

        self._offense, self._offense_score, self._defense, self._defense_score = self._parse_sides(html)

        minutes, seconds = html.find('span', class_='drive-details').text.split(',')[-1].split(':')
        self._seconds = 60 * int(minutes) + int(seconds)

        self._plays = self._parse_plays(html)

    @property
    def plays(self):
        return self._plays

    @property
    def offense_score(self):
        return self._offense_score

    @property
    def defense_score(self):
        return self._defense_score

    @property
    def offense(self):
        return self._offense

    @property
    def defense(self):
        return self._defense

    def _parse_plays(self, html):
        """
        Parses the plays for this drive
        :param html: html for the drive
        :return: yields the plays in the drive
        """
        for play in html.find_all('li'):
            header = play.find('h3').text.strip()
            text = play.find('p').text.strip()

            if _should_skip(header):
                continue

            try:
                yield parse_play(header, text, self._offense)
            except Exception as e:
                logger.info("Error parsing: {header} {text} because {error}"
                            .format(header=header, text=text, error=e.message))
                yield None

    @staticmethod
    def _parse_sides(html):
        """
        Find which team is on offense and which is on defense, and their scores (after this drive)
        :param html: html for the drive
        :return: offensive team, offense score, defensive team, defense score
        """
        offense_name = str.upper(re.findall('nfl/500/[a-z]*\.png', html.find('img').get('src'))[0][8:-4])

        home_team = html.find('span', class_='home').find('span', class_='team-name').text
        away_team = html.find('span', class_='away').find('span', class_='team-name').text

        home_score = int(html.find('span', class_='home').find('span', class_='team-score').text)
        away_score = int(html.find('span', class_='away').find('span', class_='team-score').text)

        if home_team == offense_name:
            offense = home_team
            defense = away_team
            offense_score = home_score
            defense_score = away_score
        else:
            assert away_team == offense_name
            offense = away_team
            defense = home_team
            offense_score = away_score
            defense_score = home_score

        return offense, offense_score, defense, defense_score


def _should_skip(header):
    """
    Identify some "plays" as non-plays
    :param header: header for the play
    :return: True if I don't want to parse this play
    """
    return str.startswith('END', header)
