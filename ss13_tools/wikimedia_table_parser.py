import sys
import pandas as pd
import requests


def main(args):
    """main() will be run if you run this script directly"""
    url = "https://wiki.ss13.co/Guide_to_Genetics"
    response = requests.get(url)

    df = pd.read_html(response.content)[0]
    df = df.sort_values(by="Mutation")
    print(df)
    df.to_csv("table.csv", sep="$")


def run():
    """Entry point for the runnable script."""
    sys.exit(main(sys.argv[1:]))


if __name__ == "__main__":
    """main calls run()."""
    run()
