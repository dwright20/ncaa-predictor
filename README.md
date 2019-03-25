# NCAA Predictor
NCAA Predictor is a project I am working on to get a better understanding of web scraping & data analysis while using Python.  I scraped the data from [https://www.sports-reference.com/cbb/](https://www.sports-reference.com/cbb/) and created the bracket (for easier result tracking) on [ESPN Tournament Challenge](http://fantasy.espn.com/tournament-challenge-bracket/2019/en/).  

**Code**:
- [Predictor](https://github.com/dwright20/ncaa-predictor/blob/master/PythonFiles/ncaa_predictor.py) - Python code for predicting who the tournament winner would be
- [Scraper](https://github.com/dwright20/ncaa-predictor/blob/master/PythonFiles/ncaa_scraper.py) - Python code for scraping tournament data since 2010
## Predictor Results
### Brackets
I created a bracket based on the results from a Random Forest Classification using NCAA Men's Basketball data scraped from the years 2010 - 2019.  I worked my way from the top of the results [table](https://github.com/dwright20/ncaa-predictor#table) to the bottom, choosing the team to advance until they faced a team that was higher than them on the table.  Once I finished going through the table, I used a combination of my own knowledge and anlyst predictions to fill in the remaining results.  Below is an image of the resulting bracket. 

![Completed Bracket]( https://github.com/dwright20/ncaa-predictor/blob/master/Brackets/generated-and-self-picks.png )
### Table
The percent probability of each team to win the championship was averaged across 10 trials and are given in the table below, ordered from greatest to least probability.  Teams with a predicted probability of 0% were omitted. 

| Gonzaga | Buffalo | North Carolina | Duke | Michigan State | Auburn | Virginia | Villanova | Prairie View | Murray State | Belmont | Liberty | Houston | VCU | Georgia State | Kansas | Tennesssee | Mississippi |
|  ----- |   ----- |  ----- |  ----- |  ----- |  ----- |  ----- |  ----- |  ----- |  ----- |  ----- |  ----- |  ----- |  ----- |  ----- |  ----- |  ----- |  ----- |
| 58.6 | 49.2 | 18.9 | 17 | 6 | 4.7 | 4 | 3.4 | < 1 | < 1 | < 1 | < 1 | < 1 | < 1 | < 1 | < 1 | < 1 | < 1 |

## Actual Results
[Results from predictor only](https://github.com/dwright20/ncaa-predictor/blob/master/Brackets/generated-picks-ro16.png):

| Ro64 | Ro32 |
| ----- | ----- |
| 13/16 | 8/13 |

