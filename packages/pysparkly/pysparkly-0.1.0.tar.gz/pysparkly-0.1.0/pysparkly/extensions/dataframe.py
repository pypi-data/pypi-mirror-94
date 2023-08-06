from pydeco import add_method
from pyspark.sql.dataframe import DataFrame
from pysparkly import parse_columns

@add_method(DataFrame)
def select_columns(self, included_pattern=None, excluded_pattern=None, columns=None, dtypes=None):
    """
    Select specific columns from dataframe.

    :param DataFrame self:
    :param list(str) included_pattern: keep columns in this list.
    :param list(str) excluded_pattern: keep columns not int this list.
    :param list(str) columns: columns to parsed, by default use dataframe's columns.
    :param list(str) dtypes: types to keep, if 'None' keep all columns.
    """
    columns_to_keep = parse_columns(self, included_pattern, excluded_pattern, columns, dtypes)
    return self.select(*list(columns_to_keep))