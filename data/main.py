import argparse
from pages import Week, BoxScore


def main(year):
    for week in range(1, 18):
        w = Week(year, week)
        for game_id in w.get_game_ids():
            b = BoxScore(game_id)
            drives = b.get_drives()
            print len(list(drives))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, help="Year of games to scrape")
    args = parser.parse_args()

    main(args.year)
