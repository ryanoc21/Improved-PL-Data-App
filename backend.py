"""
This file contains the backend of the premier league web app where the webscraping
and data processing are performed.
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup


class DataProcess:
    def __init__(self, standings_url):
        self.standings_url = standings_url

    def scrape(self):
        """
        Scrapes data from the standings table on fbref.com
        :return: a list containing links to data for all squads
        """
        data = requests.get(self.standings_url)

        # Instantiate the beautifulsoup class
        soup = BeautifulSoup(data.text,'lxml')

        # Parse the data for the table
        standings_table = soup.select('table.stats_table')[0]

        # Only retrieve the anchor tags from the table
        links = standings_table.find_all('a')

        # Get the href from the anchor tag
        links = [l.get('href') for l in links]

        # Get the squad links
        squad_links = [l for l in links if '/squads/' in l]
        squad_links = [f"https://fbref.com{l}" for l in squad_links]
        return squad_links

    def retrieve_link(self,team):
        """
        Retrieves the link for the squad the user requires data on
        :param team: String of desired team
        :return: The link to the data page for the team parameter
        """
        for squad in self.scrape():
            if f"/{team}" in squad:
                return squad
            else:
                continue

    # def retrieve_data(self,link,required_data):
    #     """
    #     Takes the required data for a team as the input and returns its corresponding dataframe
    #     :param link: The link to the team the user will require data for
    #     :param required_data: The required team data the user will need
    #     :return: A pandas dataframe of the required data
    #     """
    #     df = pd.read_html(link,match=required_data)[0]
    #     return df



