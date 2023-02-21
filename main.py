import streamlit as st
from backend import DataProcess
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date

# URL for the website
standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

# The interactive elements of the app
col1, col2 = st.columns(2)

with col1:
    st.image("football.png", width=300)

with col2:
    st.title("Premier League Data App")
    message = """
    A Premier League app that displays important data for every squad. The data are scraped from fbref.com using
    the BeautifulSoup module in Python. Processing was performed using pandas. The source code can be seen [here]
    (https://github.com/ryanoc21/Improved-PL-Data-App)
    
    """
    st.write(message)
    st.write("""
    NOTE: The calculations may take a while because the program scrapes the site on every iteration. 
    """)

team = st.selectbox("Pick a team",
                    ("Select", "Arsenal", "Liverpool", "Manchester-City", "Manchester-United",
                     "Newcastle-United", "Tottenham", "Brighton", "Fulham", "Brentford",
                     "Chelsea", "Aston-Villa", "Crystal-Palace", "Nottingham-Forest",
                     "Leicester-City", "Leeds-United", "West-Ham", "Wolverhampton-Wanderers",
                     "Bournemouth", "Everton", "Southampton"))

metric = st.selectbox("Pick a metric",
                      ('Goals', "Shooting", "Goalkeeping"))
# Instantiate DataProcess object
data = DataProcess(standings_url)

if team != "Select":

    data.scrape()
    if metric == "Goals":
        # ----------Start of code for summary stats of goals scored and conceded ----------
        scores_fixtures = pd.read_html(data.retrieve_link(team), match="Scores & Fixtures")[0]
        drop_list = ['EFL Cup', 'FA Cup', 'Champions League', 'Community Shield']
        scores_fixtures = scores_fixtures[scores_fixtures.Comp.isin(drop_list) == False]

        # Change goals for values to int and dropna
        scores_fixtures['GF'] = scores_fixtures['GF'].fillna(0)
        scores_fixtures['GF'] = scores_fixtures['GF'].astype('int')
        # Change goals against values to int and dropna
        scores_fixtures['GA'] = scores_fixtures['GA'].fillna(0)
        scores_fixtures['GA'] = scores_fixtures['GA'].astype('int')

        # Write calculations in the app
        st.write(f"{team} have averaged {np.round(scores_fixtures['GF'].mean(), 2)} per game.")
        st.write(f"{team} have conceded an average of {np.round(scores_fixtures['GA'].mean(), 2)} per game.")
        # ----------End of code for summary stats of goals scored and conceded ----------

        # ----------Start of code for plotting top scorers ----------
        # Read the html
        standard = pd.read_html(data.retrieve_link(team), match='Standard Stats')[0]

        # Drop the multilevel column
        standard.columns = standard.columns.droplevel()

        # Change the name of the first Gls column to Goals as there is two
        standard.columns.values[8] = 'Goals'

        # Make a new dataframe containing players and the goals they scored
        scorers = standard[['Player', 'Goals']]

        # Drop anyone who hasn't scored
        scorers = scorers[scorers.Goals > 0]

        # Drop the last two rows which contains squad totals
        scorers = scorers.iloc[:-2]

        # Sort the values and reverse the dataframe so the plot looks well
        scorers = scorers.sort_values(by='Goals')
        scorers = scorers.reindex(index=scorers.index[::-1])

        # Plot the scorers
        fig = px.bar(scorers, x='Player', y='Goals',
                     title=f"Top Scorers as of {date.today()}",
                     labels={
                         'GoalsNo': 'Number of Goals',
                         'Name': 'Player'
                     }
                     )
        st.plotly_chart(fig)

    elif metric == "Shooting":
        st.write("This section is in progress")
    else:
        st.write("This section is in progress")
