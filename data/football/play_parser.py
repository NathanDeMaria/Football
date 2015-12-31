from .plays import StandardPlay, Kickoff


def parse_play(header, text, offense):
    """
    Convert the header
    :param header: play header, like 1st and 10 at SEA 11
    :param text: play body, like (14:40 - 1st) P.Manning pass deep left to D.Thomas for a TOUCHDOWN
    :param offense: offensive team
    :return: correct play object
    """
    if header == '':
        return Kickoff(text)
    else:
        return StandardPlay(header, text, offense)
