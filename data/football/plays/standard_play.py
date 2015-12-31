from .play import Play


class StandardPlay(Play):
    def __init__(self, header, text, offense):
        """
        Scrape out a normal play
        :param header: play header, like 1st and 10 at SEA 11
        :param text: body of the play
        :param offense: offensive team name
        """
        Play.__init__(self, text)

        tokens = header.split(' ')
        down = tokens[0]
        dist = tokens[2]

        if tokens[4] == '50':
            self._field_position = 50
        else:
            self._field_position = _convert_field_position(tokens[4], tokens[5], offense)

        self._down = int(down[0])
        self._distance = int(dist)

    @property
    def down(self):
        return self._down

    @property
    def distance(self):
        return self._distance

    @property
    def field_position(self):
        return self._field_position


def _convert_field_position(team, yardline, offense):
    """
    Gets the field position for a play
    :param team: team whose side of the field it's on
    :param yardline: yardline of the
    :param offense: offensive team
    :return: field position (yards left to a TD)
    """
    yard = int(yardline)
    if team == offense:
        return 100 - yard
    else:
        return yard
