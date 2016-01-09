import argparse
from csv import DictWriter

from football.logger import logger
from football.pages import Week, PlayByPlay
from football.plays import StandardPlay


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
            final_lookup = {
                p.home: p.home_score,
                p.away: p.away_score
            }

            drives = list(p.get_drives())
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
                                   drive_number=i, game_id=game_id, offense=drive.offense, defense=drive.defense,
                                   offense_final=final_lookup[drive.offense], defense_final=final_lookup[drive.defense])
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
