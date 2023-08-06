import pandas as pd
from sklearn.externals import joblib


def score(data_conf, model_conf, **kwargs):
    predict_df = pd.read_csv(data_conf['location'])
    features = 'sepallength,sepalwidth,petallength,petalwidth'.split(',')
    X_test = predict_df.loc[:, features]
    y_test = predict_df['class']

    model = joblib.load('artifacts/input/iris_knn.joblib')

    y_pred = model.predict(X_test)

    print("Finished Scoring")

    # store predictions somewhere.. As this is demo, we'll just print to stdout.
    print(y_pred)

    return X_test, y_pred, y_test, model
