import re


class Play:
    # NOTE: this constructor shouldn't be called, I'm just making it to make PyCharm happy
    # Instead, use the constructors
    def __init__(self, text):
        """
        Parses out the start time of the play
        :param text: something starting with \t\t\t...(15:00 - 1st)
        """
        time, quarter = re.findall('\([0-9]{1,2}:[0-9]{2} - [1-4stndrhOT]{2,3}\)', text)[0][1:-1].split('-')
        minutes, seconds = time.split(':')
        self._seconds = 60 * int(minutes) + int(seconds)

        quarter_text = quarter.strip()

        if quarter_text == 'OT':
            self._quarter = 5
        else:
            self._quarter = int(quarter_text[0])

    @property
    def seconds(self):
        return self._seconds

    @property
    def quarter(self):
        return self._quarter
