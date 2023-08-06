import pandas as pd 
from pathlib import Path

def load_soilmoisture(n_features=[1,7,8,9], target=-1, n_instances=12130, return_dataset=False):
    """
    Loads the a multivariate dataset that is well suited to regression
    tasks. The dataset contains 12130 instances and 11 columns:
    - datetime
    - 6 soil moisture measurements (at 7cm), measured by low cost capacitive sensors (soil_moisture_c0 .. soil_moisture_c5)
    - Soil temperature
    - Air temperature
    - Air humidity (relative humidity)
    - Volumetric water content (target), measured with hydraprobe 2 sensor
    
    Parameters
    ----------
    n_features : list of ints, default=(1,7,8,9) 
        The columns to be used as features. 
    target : int, default=-1.
        The column to use as target
    n_instances : int, default=12130
        The length of the dataset.
    return_dataset : bool, default=False
        Return the complete raw dataset as a pandas dataframe object instead of X and y pandas series to
        get access to alternative targets, extra features, content and meta. 
    Returns
    -------
    X : dataframe with shape (n_instances, n_features) if return_dataset=False
        A pandas DataFrame describing the instance features.
    y : pandas series with shape (n_instances,) if return_dataset=False
        the pandas Series describing the target vector will be in X.
    dataset : Pandas Dataset instance if return_dataset=True
    """
    
    sm_file = Path.cwd() / "data" / "soil_moisture_example1.pkl"
    soil_moisture_df = pd.read_pickle(str(sm_file.resolve()))
    X = soil_moisture_df.iloc[:n_instances,n_features]
    y = soil_moisture_df.iloc[:n_instances,[target]]
    if return_dataset:
        return soil_moisture_df
    return(X,y)
