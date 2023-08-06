
from predictions_analyzer.tabular import *
from sklearn.metrics import accuracy_score

classification_data_path = "./test_datasets/classification/"

def get_ExClfObj():
    ex = ClassificationAnalyzer(simulate_data=True)

    ex.fit_models()
    ex.predict()

    return ex

def get_JSObj():
    js = ClassificationAnalyzer(simulate_data = False,
                                multi_output=True)
    ycols = ['resp', 'resp_1', 'resp_2', 'resp_3', 'resp_4']

    X = pd.read_csv(classification_data_path + "js_sample_multi.csv")
    y = X[ycols]

    X = X.drop(ycols, axis = 1).fillna(X.mean())

    js.load_unsplit_data(X, y)
    print(js.X.shape)
    print(js.y.shape)

    js.split_val_train(method = "multi_stochastic")
    print("After Splits")
    print(js.X_train.shape)
    print(js.y_train.shape)
    print(js.X_valid.shape)
    print(js.y_valid.shape)

    js.initialize_wandb(project_name="predictions_analyzer_tests",
                         group_name= "js_test_wandb_fit_predict_multi")

    return js

def test_wandb_fit_predict_multi():
    js = get_JSObj()

    js.fit_predict_log_wandb_multi()


def get_all_test_objs():
    pass


def test_validation_splits_arent_the_same():
    """
    Check that the stochastic method
    and time series method produce
    different results.

    :return:
    """
    pass

def get_titanic_obj():
    titanic = ClassificationAnalyzer(simulate_data=False)

    X = pd.read_csv(classification_data_path + "titanic.csv")

    y = X.pop("Survived")

    titanic.load_unsplit_data(X, y)
    print(titanic.X.shape)
    print(titanic.y.shape)

    titanic.split_val_train()

    # print(titanic.X_train.shape)
    #print(titanic.y_train.shape
    #print(titanic.X_valid.shape)
    #print(titanic.y_valid.shape)

    titanic.fit_models()
    titanic.predict()

    return titanic

def get_titanic_obj_stochastic_splits():
    titanic = ClassificationAnalyzer(simulate_data=False)
    X = pd.read_csv(classification_data_path + "titanic.csv")
    y = X.pop("Survived")

    titanic.load_unsplit_data(X, y)
    print(titanic.X.shape)
    print(titanic.y.shape)

    titanic.split_val_train(method = "stochastic")

    # print(titanic.X_train.shape)
    # print(titanic.y_train.shape
    # print(titanic.X_valid.shape)
    # print(titanic.y_valid.shape)

    titanic.fit_models()
    titanic.predict()

    return titanic

def test_titanic_stochastic():
    titanic_stochastic = get_titanic_obj_stochastic_splits()

def fetal_obj():
    pass

def test_apply_ytrue():
    ex = get_ExClfObj()
    titanic = get_titanic_obj()

    print("Testing with Generated Data")
    accuracy = ex.apply_ytrue(func = accuracy_score,
                                 func_name = "accuracy_score")

    print(accuracy)
    print(accuracy.shape)


    print("Testing with Titanic Data")

    accuracy = titanic.apply_ytrue(func=accuracy_score,
                              func_name="accuracy_score")
    print(accuracy)
    print(accuracy.shape)


def test_add_to_metrics_from_ytrue_and_preds_df():
    ex = get_ExClfObj()
    titanic = get_titanic_obj()
    titanic_stochastic = get_titanic_obj_stochastic_splits()

    test_objects = [("simulated", ex), ("titanic", titanic),
                    ("titanic_stochastic", titanic_stochastic)]

    for name, obj in test_objects:
        print("\nTesting: ", name, " dataset")

        obj.add_to_metrics_from_ytrue_and_preds_df(func = accuracy_score,
                                                  func_name = "accuracy_score")

        print(obj.metrics_df)

        assert obj.metrics_df.empty != True  # Assert dataframe is not empty.


def test_fit_accuracy_scores():
    ex = get_ExClfObj()
    titanic = get_titanic_obj()

    test_objects = [("simulated", ex), ("titanic", titanic)]

    for name, obj in test_objects:
        print("\nTesting: ", name, " dataset")
        obj.fit_accuracy_scores()

        accuracy_score_df = obj.metrics_df.loc["accuracy_score"]

        print(accuracy_score_df)
        print(accuracy_score_df.shape)

        # Assert accuracy_score is only one row.
        # assert accuracy_score_df.shape == tuple(len(ex.models), )


def test_validate_classification_constructor():

    X, y = get_classification()


def test_ExampleAnalyzerConstructor():
    assert ClassificationAnalyzer()

def test_fit_predict():
    ex = get_ExClfObj()

    print(ex.preds_df)
    print(ex.preds_df.shape)

def test_fit_class_metrics():
    ex = get_ExClfObj()

    ex.get_classification_metrics()

    print(ex.metrics_df)

    # Assert ex.metrics_df is empty!


def test_mean_ensemble():
    ex = get_ExClfObj()

    ex.fit_mean_ensemble()

    print(ex.ensembled_preds_df)

    assert ex.ensembled_preds_df.empty != True

    # Assert there is only one mean column!

def test_median_ensemble():
    ex = get_ExClfObj()
    titanic = get_titanic_obj()

    test_objects = [("simulated", ex), ("titanic", titanic)]

    for name, obj in test_objects:
        print("\nTesting: ", name, " dataset")

        obj.fit_median_ensemble()
        print(obj.ensembled_preds_df)
        assert obj.ensembled_preds_df.empty != True

    # Assert there is only one mean column!

def test_mode_ensemble():

    # TODO: Not working yet for some reason.

    ex = get_ExClfObj()

    ex.fit_mode_ensemble()

    print(ex.ensembled_preds_df)

    assert ex.ensembled_preds_df.empty != True

    # Assert there is only one mean column!

def test_show_confusion_matrix():
    ex = get_ExClfObj()
    titanic = get_titanic_obj()

    test_objects = [("simulated", ex), ("titanic", titanic)]

    for name, obj in test_objects:
        print("\nTesting: ", name, " dataset")

        obj.show_confusion_matrix()

def test_show_classification_report():
    ex = get_ExClfObj()
    titanic = get_titanic_obj()

    test_objects = [("simulated", ex), ("titanic", titanic)]

    for name, obj in test_objects:
        print("\nTesting: ", name, " dataset")

        obj.show_classification_report()

def test_all_stat_ensembled_pred_metrics():
    ex = get_ExClfObj()
    titanic = get_titanic_obj()

    test_objects = [("simulated", ex), ("titanic", titanic)]

    for name, obj in test_objects:
        print("\nTesting: ", name, " dataset")

        obj.fit_all_stats_ensembles()

        print(obj.ensembled_preds_df)

        # Assert it is not an empty dataframe.
        assert obj.ensembled_preds_df.empty != True

        # Assert no NaNs are in the predictions.
        assert obj.ensembled_preds_df.isna().sum().sum() == 0

def test_show_models():
    ex = get_ExClfObj()
    titanic = get_titanic_obj()

    test_objects = [("simulated", ex), ("titanic", titanic)]

    for name, obj in test_objects:
        print("\nTesting: ", name, " dataset")

        obj.show_models()

def test_ensembled_preds_metrics_exist():
    ex = get_ExClfObj()
    titanic = get_titanic_obj()

    test_objects = [("simulated", ex), ("titanic", titanic)]

    for name, obj in test_objects:
        print("\nTesting: ", name, " dataset")

        obj.fit_mean_ensemble()

        print(obj.ensembled_preds_df)

        obj.add_to_metrics_from_ytrue_and_preds_df(
            func = accuracy_score,
            func_name = "accuracy_score"
        )

        print(obj.metrics_df)

        assert obj.metrics_df.empty != True

    # BUG: when adding ensembles, it adds another row.
    # TO DO:
    # assert accuracy_score is in one row.

def test_show_feature_analysis_from_model():
    ex = get_ExClfObj()
    titanic = get_titanic_obj()

    test_objects = [("simulated", ex), ("titanic", titanic)]

    for name, obj in test_objects:
        print("\nTesting: ", name, " dataset")

        obj.show_feature_analysis_from_model()



def test_wandb_fit_predict():
    ex = get_ExClfObj()
    titanic = get_titanic_obj()

    test_objects = [("simulated", ex), ("titanic", titanic)]

    wandb.login()

    for name, obj in test_objects:
        print("\nTesting: ", name, " dataset")

        obj.show_models()

        obj.initialize_wandb(project_name="predictions_analyzer_tests",
                             group_name=name+"_test_wandb_fit_predict",
                             experiment_name="testing")

        obj.fit_predict_log_wandb()

def test_find_hardest_samples():
    ex = get_ExClfObj()
    titanic = get_titanic_obj()

    test_objects = [("simulated", ex), ("titanic", titanic)]

    for name, obj in test_objects:
        print("\nTesting: ", name, " dataset")

        obj.find_hardest_samples()

        # Assert that obj.preds_df

        # Assert that not all outputs are 0
        # Assert that the output of n_correct is not 0 len(X)

        # Assert all values in self.trues_df?


def test_show_all_reports():
    ex = get_ExClfObj()
    titanic = get_titanic_obj()

    test_objects = [("simulated", ex), ("titanic", titanic)]

    for name, obj in test_objects:
        print("\nTesting: ", name, " dataset")
        obj.show_all_reports()

def test_valid_split_random():
    ex = get_ExClfObj()
    titanic = get_titanic_obj()

    test_objects = [("simulated", ex), ("titanic", titanic)]

    for name, obj in test_objects:
        print("\nTesting: ", name, " dataset")
        obj.show_all_reports()