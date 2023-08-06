def filter_FN(prediction_series, truth_series, truth_df, threshold=0.5):
    """ Parameters:
        prediction_series: The prediction values
        truth_series: The truth values
        truth_df: The dataframe you want to sample from
        threshold: The round-up-limit for classification for the predictions

        Returns: a filtered dataframe
    """
    pred = prediction_series > threshold
    return truth_df.query('@truth_series != @pred and @truth_series == True')

def filter_FP(prediction_series, truth_series, truth_df, threshold=0.5):
    """ Parameters:
        prediction_series: The prediction values
        truth_series: The truth values
        truth_df: The dataframe you want to sample from
        threshold: The round-up-limit for classification for the predictions

        Returns: a filtered dataframe
    """
    pred = prediction_series > threshold
    return truth_df.query('@truth_series != @pred and @truth_series == False')

def filter_TP(prediction_series, truth_series, truth_df, threshold=0.5):
    """ Parameters:
        prediction_series: The prediction values
        truth_series: The truth values
        truth_df: The dataframe you want to sample from
        threshold: The round-up-limit for classification for the predictions

        Returns: a filtered dataframe
    """
    pred = prediction_series > threshold
    return truth_df.query('@truth_series == @pred and @truth_series == True')

def filter_TN(prediction_series, truth_series, truth_df, threshold=0.5):
    """ Parameters:
        prediction_series: The prediction values
        truth_series: The truth values
        truth_df: The dataframe you want to sample from
        threshold: The round-up-limit for classification for the predictions

        Returns: a filtered dataframe
    """
    pred = prediction_series > threshold
    return truth_df.query('@truth_series == @pred and @truth_series == False')
