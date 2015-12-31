from .play import Play


class Kickoff(Play):
    def __init__(self, text):
        """
        Kickoffs are plays too
        :param text:  the body of the play
        """
        Play.__init__(self, text)
