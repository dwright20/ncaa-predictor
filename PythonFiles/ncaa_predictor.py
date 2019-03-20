from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import cross_val_score
from scipy.stats import zscore


def RandomForest():
    first_csv = '~/Documents/NCAAStats/2010.csv'
    # list of col names we don't want to standardize
    unique_cols = ['Champion?', '%', 'SOS', 'SRS', 'Seed', 'Power Conference?']
    all_data = pd.read_csv(first_csv)  # initialize data to append other years too
    del all_data['Unnamed: 0']
    del all_data['Team']
    # only standardize all columns that aren't percentages, uniquely calculated values, or categorical
    for col in all_data.columns:
        if not any(uniq in col for uniq in unique_cols):
            all_data[col] = zscore(all_data[col])
    for i in range(2011, 2019):
        in_path = '~/Documents/NCAAStats/' + str(i) + '.csv'
        data = pd.read_csv(in_path)
        del data['Unnamed: 0']
        del data['Team']
        for col in data.columns:
            if not any(uniq in col for uniq in unique_cols):
                data[col] = zscore(data[col])
        all_data = all_data.append(data)  # add to existing data

    classification_data = all_data['Champion?']  # data of value aiming to classify

    predictor_data = all_data.copy()  # data to evaluate for classification
    del predictor_data['Champion?']

    n_estimators = 1000
    max_features = None
    bootstrap = True
    n_jobs = -1

    clf = RandomForestClassifier(
        n_estimators=n_estimators,
        max_features=max_features,
        bootstrap=bootstrap,
        n_jobs=n_jobs,
    )

    clf.fit(predictor_data, classification_data)  # evaluation data, target classification

    recall = cross_val_score(clf, predictor_data, classification_data, scoring='recall', cv=5)
    accuracy = cross_val_score(clf, predictor_data, classification_data, scoring='accuracy', cv=5)
    f1 = cross_val_score(clf, predictor_data, classification_data, scoring='f1_micro', cv=5)
    precision = cross_val_score(clf, predictor_data, classification_data, scoring='precision_micro', cv=5)

    # print various cross val scores
    print('Recall {}\n'.format(recall))
    print('Accuracy {}\n'.format(accuracy))
    print('F1 {}\n'.format(f1))
    print('Precision {}\n'.format(precision))

    # Get teams to predict from
    teams_path = '~/Documents/NCAAStats/2019.csv'
    teams_data = pd.read_csv(teams_path)
    del teams_data['Unnamed: 0']

    # print all teams and their index - used initially to pair with probabilities
    for i in range(68):
        print('{}. {}'.format(i, teams_data.iloc[i][teams_data.columns.get_loc('Team')]))

    del teams_data['Team']  # Drop Team name col
    del teams_data['Champion?']  # Drop Champion col

    for col in teams_data.columns:
        if not any(uniq in col for uniq in unique_cols):
            teams_data[col] = zscore(teams_data[col])

    # print index of team who is predicted to win
    predictions = clf.predict(teams_data)
    for index, prediction in enumerate(predictions):
        if prediction == 1:
            print('{}. {}'.format(index, prediction))

    # print predicted probabilities of team winning
    probabilities = clf.predict_proba(teams_data)
    for index, probability in enumerate(probabilities):
        print('{}'.format(probability))

if __name__ == "__main__":
    RandomForest()