import argparse
from pages import Week


def main(year):
    for week in range(1, 18):
        w = Week(year, week)
        print list(w.get_game_ids())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, help="Year of games to scrape")
    args = parser.parse_args()

    main(args.year)
