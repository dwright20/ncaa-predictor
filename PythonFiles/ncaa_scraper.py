import math
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

# dictionary of 2019 teams and their seeds
teams_2019 = {
    'abilene-christian': 15,
    'arizona-state': 11,
    'auburn': 5,
    'baylor': 9,
    'belmont': 11,
    'bradley': 15,
    'buffalo': 6,
    'cincinnati': 7,
    'colgate': 15,
    'duke': 1,
    'fairleigh-dickinson': 16,
    'florida': 10,
    'florida-state': 4,
    'gardner-webb': 16,
    'georgia-state': 14,
    'gonzaga': 1,
    'houston': 3,
    'iona': 16,
    'iowa': 10,
    'iowa-state': 6,
    'kansas': 4,
    'kansas-state': 4,
    'kentucky': 2,
    'liberty': 12,
    'louisville': 7,
    'louisiana-state': 3,
    'marquette': 5,
    'maryland': 6,
    'michigan': 2,
    'michigan-state': 2,
    'minnesota': 10,
    'mississippi-state': 5,
    'montana': 15,
    'murray-state': 12,
    'nevada': 7,
    'new-mexico-state': 12,
    'north-carolina': 1,
    'north-carolina-central': 16,
    'north-dakota-state': 16,
    'northeastern': 13,
    'northern-kentucky': 14,
    'ohio-state': 11,
    'oklahoma': 9,
    'old-dominion': 14,
    'mississippi': 8,
    'oregon': 12,
    'prairie-view': 16,
    'purdue': 3,
    'saint-louis': 13,
    'seton-hall': 10,
    'st-johns-ny': 11,
    'saint-marys-ca': 11,
    'syracuse': 8,
    'temple': 11,
    'tennessee': 2,
    'texas-tech': 3,
    'california-irvine': 13,
    'central-florida': 9,
    'utah-state': 8,
    'virginia-commonwealth': 8,
    'vermont': 13,
    'villanova': 6,
    'virginia': 1,
    'virginia-tech': 4,
    'washington': 9,
    'wisconsin': 5,
    'wofford': 7,
    'yale': 14
}

# method that takes in a list of teams and a year and parses through them compiling data for each tournament competitor
# for given year
def ScrapeYear (urls, year):
    print('Scraping stats for {}'.format(year))
    team_url = 'https://www.sports-reference.com'
    path = '~/Documents/NCAAStats/' + str(year) + '.csv'  # path where csv is written for retrieval later
    data = []
    for url in urls:
        temp_url = team_url + url
        team = url.split('/')[3]
        team_req = requests.get(temp_url).content

        champion = 1 if b'NCAA Champion' in team_req else 0  # determine if team won championship

        # Soup individual team request to find text summaries above tables
        team_soup = BeautifulSoup(team_req, 'lxml')
        stat_summaries = team_soup.find('div', {'id': 'info'}).findAll('p')
        text_summaries = []

        for element in stat_summaries:
            text_summaries.append(element.findAll(text=True))

        overall = re.findall('\d{1,2}-\d{1,2}', str(text_summaries[2]))[0]  # overall win-loss
        overall_games = overall.split('-')
        overall_percent = int(overall_games[0]) / (int(overall_games[0]) + int(overall_games[1]))  # overall win %

        # formatting different for 2016 syracuse and teams after 2018
        if year >= 2018 or (year == 2016 and team == 'syracuse'):
            conference_name = re.findall('in \D+', str(text_summaries[2]))[0]  # conference not on own line, must parse
            conference_names = conference_name.split('\'')
            conference = conference_names[2]  # conference
            conference_wl = re.findall('\d{1,2}-\d{1,2}', str(text_summaries[2]))[1]  # conference win-loss
            conference_games = conference_wl.split('-')
            conference_percent = int(conference_games[0]) / (int(conference_games[0]) + int(conference_games[1]))  # conference win %
            srs = re.findall('\d+.\d+', str(text_summaries[6]))[0]  # srs
            sos = re.findall('\d+.\d+', str(text_summaries[7]))[0]  # sos
            ortg = re.findall('\d+.\d+', str(text_summaries[8]))[0]  # ortg
            drtg = re.findall('\d+.\d+', str(text_summaries[9]))[0]  # drtg

            if year == 2019:
                seed = teams_2019[team]
            else:
                seed = re.findall('#\d+ seed', str(text_summaries[10]))[0]
                seed = re.sub('[^0-9]', '', str(seed))  # tournament seed
        else:
            conference = str(text_summaries[3][2])  # conference
            conference_wl = re.findall('\d{1,2}-\d{1,2}', str(text_summaries[3]))[0]  # conference win-loss
            conference_games = conference_wl.split('-')
            conference_percent = int(conference_games[0]) / (int(conference_games[0]) + int(conference_games[1]))  # conference win %
            srs = re.findall('\d+.\d+', str(text_summaries[7]))[0]  # srs
            sos = re.findall('\d+.\d+', str(text_summaries[8]))[0]  # sos
            ortg = re.findall('\d+.\d+', str(text_summaries[9]))[0]  # ortg
            drtg = re.findall('\d+.\d+', str(text_summaries[10]))[0]  # drtg
            seed = re.findall('#\d+ seed', str(text_summaries[11]))[0]
            seed = re.sub('[^0-9]', '', str(seed))  # tournament seed

        # determine if team is part of historically dominant conferences
        isPowerConf = 1 if conference == 'ACC' or conference == 'SEC' or conference == 'Big East' else 0

        team_tables = pd.read_html(team_req)

        roster = team_tables[0]  # roster table
        stats = team_tables[1]  # team and opponent stats table

        fr = roster['Class'].value_counts()['FR'] if 'FR' in roster['Class'].values else 0
        so = roster['Class'].value_counts()['SO'] if 'SO' in roster['Class'].values else 0
        jr = roster['Class'].value_counts()['JR'] if 'JR' in roster['Class'].values else 0
        sr = roster['Class'].value_counts()['SR'] if 'SR' in roster['Class'].values else 0

        underclassmen = fr + so  # total number of underclassmen
        upperclassmen = jr + sr  # total number of upperclassmen

        # changes height into inches
        def parse_height(x):
            heights = str(x).split('-')
            if math.isnan(float(heights[0])): return 0  # return if value not given
            feet_to_inches = int(heights[0]) * 12
            total = feet_to_inches + int(heights[1])
            return total

        roster['Height'] = roster['Height'].apply(lambda x: parse_height(x))  # parses heights into inches
        avg_height = pd.to_numeric(roster['Height']).mean()  # finds average of team's height in inches

        # add dictionary of data to a list of teams for year
        data.append({
            'Team': team, 'Win %': overall_percent, 'Power Conference?': isPowerConf,
            'Conf Win %': conference_percent, 'SRS': srs, 'SOS': sos,
            'ORTG': ortg, 'DRTG': drtg, 'Seed': seed,
            '# Underclassmen': underclassmen, '# Upperclassmen': upperclassmen, 'Avg Height': avg_height,
            'Team FG': stats.iloc[0][3], 'Team FGA': stats.iloc[0][4], 'Team FG%': stats.iloc[0][5],
            'Team 2P': stats.iloc[0][6], 'Team 2PA': stats.iloc[0][7], 'Team 2P%': stats.iloc[0][8],
            'Team 3P': stats.iloc[0][9], 'Team 3PA': stats.iloc[0][10], 'Team 3P%': stats.iloc[0][11],
            'Team FT': stats.iloc[0][12], 'Team FTA': stats.iloc[0][13], 'Team FT%': stats.iloc[0][14],
            'Team ORB': stats.iloc[0][15], 'Team DRB': stats.iloc[0][16], 'Team TRB': stats.iloc[0][17],
            'Team AST': stats.iloc[0][18], 'Team STL': stats.iloc[0][19], 'Team BLK': stats.iloc[0][20],
            'Team TOV': stats.iloc[0][21], 'Team PF': stats.iloc[0][22], 'Team PTS': stats.iloc[0][23],
            'Team PTS/G': stats.iloc[0][24], 'Opponent FG': stats.iloc[2][3], 'Opponent FGA': stats.iloc[2][4],
            'Opponent FG%': stats.iloc[2][5], 'Opponent 2P': stats.iloc[2][6], 'Opponent 2PA': stats.iloc[2][7],
            'Opponent 2P%': stats.iloc[2][8], 'Opponent 3P': stats.iloc[2][9], 'Opponent 3PA': stats.iloc[2][10],
            'Opponent 3P%': stats.iloc[2][11], 'Opponent FT': stats.iloc[2][12], 'Opponent FTA': stats.iloc[2][13],
            'Opponent FT%': stats.iloc[2][14], 'Opponent ORB': stats.iloc[2][15], 'Opponent DRB': stats.iloc[2][16],
            'Opponent TRB': stats.iloc[2][17], 'Opponent AST': stats.iloc[2][18], 'Opponent STL': stats.iloc[2][19],
            'Opponent BLK': stats.iloc[2][20], 'Opponent TOV': stats.iloc[2][21], 'Opponent PF': stats.iloc[2][22],
            'Opponent PTS': stats.iloc[2][23], 'Opponent PTS/G': stats.iloc[2][24], 'Champion?': champion
        })

    # turn data into Pandas DataFrame and save it as a csv
    final_frame = pd.DataFrame(data)
    final_frame.to_csv(path)
    print('Stats for {} saved to system'.format(year))

# runner method for scraping NCAA basketball data
def ParseYears ():
    start_year = 2010  # first year website tracks all data wanted
    end_year = 2020
    for i in range(start_year, end_year):
        url = "https://www.sports-reference.com/cbb/seasons/" + str(i) + "-school-stats.html"
        all_teams_req = requests.get(url).content
        soup = BeautifulSoup(all_teams_req, 'lxml')
        all_teams = soup.find_all('sup')  # find tourney teams from all teams during season
        tourney_teams = [par.parent.a for par in all_teams]  # find all html link tags for tourney teams
        teams_urls = [link.get('href') for link in tourney_teams]  # find all links of tourney teams
        ScrapeYear(teams_urls, i)  # pass teams urls and year into method to scrub their data

if __name__ == "__main__":
    ParseYears()

