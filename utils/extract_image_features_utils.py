"""
This file holds functions to extract image features from the outputted sqlite file from CellProfiler. These functions are based on the functions from the
cells.SingleCells class in Pycytominer.
"""

import pandas as pd
from sqlalchemy import create_engine
import numpy as np


def load_sqlite_as_df(
    sqlite_file_path: str,
    image_table_name: str = "Per_Image",
) -> pd.DataFrame:
    """
    load in table with image feature data from sqlite file

    Parameters
    ----------
    sqlite_file_path : str
        string of path to the sqlite file
    image_table_name : str
        string of the name with the image feature data (default = "Per_Image")

    Returns
    -------
    pd.DataFrame:
        dataframe containing image feature data
    """
    image_df = pd.read_sql_table(image_table_name, sqlite_file_path)

    return image_df


def extract_image_features(image_feature_categories, image_df, image_cols, strata):
    """Confirm that the input list of image features categories are present in the image table and then extract those features.
    This is pulled from Pycytominer cyto_utils util.py and editted.

    Parameters
    ----------
    image_feature_categories : list of str
        Input image feature groups to extract from the image table including the prefix 
        (e.g. ["Image_Correlation", "Image_ImageQuality"])
    image_df : pandas.core.frame.DataFrame
        Image dataframe from SQLite file.
    image_cols : list of str
        Columns to select from the image table.
    strata :  list of str
        The columns to groupby and aggregate single cells (for Pycytominer). In this case, we use this to make sure 
        that all identifiers for a cell to find what image it comes from are in the output.
    Returns
    -------
    image_features_df : pandas.core.frame.DataFrame
        Dataframe with extracted image features.
    """
    # Extract Image features from image_feature_categories
    image_features = list(
        image_df.columns[
            image_df.columns.str.startswith(tuple(image_feature_categories))
        ]
    )

    # Add image features to the image_df
    image_features_df = image_df[image_features]

    # Add image_cols and strata to the dataframe
    image_features_df = pd.concat(
        [image_df[list(np.union1d(image_cols, strata))], image_features_df], axis=1
    )

    return image_features_df
