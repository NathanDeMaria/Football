import re

from football.scraper import get_page


class Week:
    _url_format = 'http://site.api.espn.com/apis/site/v2/sports/football/nfl/' \
                  'scoreboard?lang=en&region=us&calendartype=blacklist&limit=100&dates={year}&seasontype=2&week={week}'

    def __init__(self, year, week):
        """
        Object that represents the weekly box scores page
        NOTE: only implemented for regular season right now
        :param year: year to get data for
        :param week: week to get data from
        """
        if not 1 <= week <= 17:
            raise ValueError("Week must be between 1 and 17 (inclusive).")

        if not 2003 <= year <= 2015:
            raise ValueError("Year must be between 2003 and 2015 (inclusive)...at least at the time of writing :)")

        url = self._url_format.format(year=year, week=week)
        self._response = get_page(url)

    def get_game_ids(self):
        """
        Scrapes the game ids out of the box score page
        :return: list of game ids
        """
        for match in re.findall('"competitions":\[\{"id":"[0-9]*', self._response):
            yield int(match[23:])
