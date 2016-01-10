import argparse
from csv import DictWriter

from football.logger import logger
from football.pages import Week, PlayByPlay


def get_plays(year):
    """
    Scrape the standard plays for given year
    :param year: year to scrape
    :return: yields dicts for each play
    """
    for week in range(1, 18):
        w = Week(year, week)
        for game_id in w.get_game_ids():
            p = PlayByPlay(game_id)
            for play_datum in p.get_play_data():
                yield play_datum
        logger.info("Completed week {0}".format(week))


def main(year):
    plays = get_plays(year)
    with open('../plays.csv', 'w') as f:
        first_play = next(plays)
        writer = DictWriter(f, first_play.keys())
        writer.writeheader()
        for play in plays:
            writer.writerow(play)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, help="Year of games to scrape")
    args = parser.parse_args()

    main(args.year)
