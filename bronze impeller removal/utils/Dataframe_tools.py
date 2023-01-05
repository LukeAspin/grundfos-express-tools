from matplotlib.mlab import psd
import pandas as pd
import numpy as np
import inspect
from pandas import DataFrame
from pandas._typing import FilePath, ReadBuffer, DtypeArg, StorageOptions
from pandas.util._decorators import Appender
from typing import Optional, overload, Literal, Sequence, Hashable, Iterable, Callable, Union, ParamSpec, Callable
from _types._types import *


class PSD:

    @overload
    def __init__(self,
                 io,
                 # sheet name is str or int -> DataFrame
                 sheet_name: str | int,
                 header: int | Sequence[int] | None = ...,
                 names=...,
                 index_col: int | Sequence[int] | None = ...,
                 usecols=...,
                 squeeze: bool | None = ...,
                 dtype: DtypeArg | None = ...,
                 engine: Literal["xlrd", "openpyxl",
                                 "odf", "pyxlsb"] | None = ...,
                 converters=...,
                 true_values: Iterable[Hashable] | None = ...,
                 false_values: Iterable[Hashable] | None = ...,
                 skiprows: Sequence[int] | int | Callable[[
                     int], object] | None = ...,
                 nrows: int | None = ...,
                 na_values=...,
                 keep_default_na: bool = ...,
                 na_filter: bool = ...,
                 verbose: bool = ...,
                 parse_dates=...,
                 date_parser=...,
                 thousands: str | None = ...,
                 decimal: str = ...,
                 comment: str | None = ...,
                 skipfooter: int = ...,
                 convert_float: bool | None = ...,
                 mangle_dupe_cols: bool = ...,
                 storage_options: StorageOptions = ...,
                 ) -> tuple[DataFrame, DataFrame, int]: ...

    @Appender(pd.read_excel.__doc__, join='')
    def __init__(self, **kwargs) -> Union[tuple[None, DataFrame, int], tuple[DataFrame, DataFrame, int]]:
        kwargs = {k: v for k, v in kwargs.items()
                  if k in inspect.signature(pd.read_excel).parameters.keys()}
        df = pd.read_excel(**kwargs)  # Reading the dataframe
        self.header_size = self._find_header_end(
            df)  # Getting the size of the header
        # Need to get the other dataframes
        psd_df = df.loc[self.header_size-1:, :]
        psd_df.reset_index(drop=True, inplace=True)
        psd_df.columns = psd_df.loc[0, :]
        psd_df.reset_index(drop=True, inplace=True)
        psd_df.columns = self._name_blank_cols(psd_df)
        ###ADDED###
        psd_df.columns = self._remove_duplicates(psd_df)
        psd_df = psd_df.drop(psd_df.index[0])
        psd_df.reset_index(drop=True, inplace=True)
        self.original_size = len(df)
        # Lets Check if we are using the header df
        self.header_data = df.loc[:self.header_size-2, :]
        self.psd_data = psd_df

    def _find_header_end(self, df: DataFrame) -> int:
        for row in df.itertuples():
            if row[1] == '[START]':
                return int(row[0])

    def _name_blank_cols(self, df):
        col = df.columns.to_list()
        count = 1
        for i, item in enumerate(col.copy()):
            if str(item) == 'nan':
                col[i] = f"No Name {count}"
                count += 1
        return col

    def _remove_duplicates(self, df):
        col = df.columns.to_list()
        arr = []
        for i, item in enumerate(col):
            if item in arr and ('Dummy '+item):
                if ('Dummy '+item) not in arr:
                    if col.count(item) > 2:
                        for i1 in range(col.count(item)):
                            arr.append('Dummy '*(i1+1)+item)
                    else:
                        arr.append('Dummy '+item)
                else:
                    continue
            else:
                arr.append(item)
        return arr


class PipeUpdates:

    def get_df(data: Union[FilePath, ReadBuffer[bytes], bytes], sheet_names: str | list[str]) -> pd.DataFrame:
        """Needing Implementation:
        1) Check if sheets are iterable or not 
        2) Check if sheets are in the excel doc
        3) Check if the data is in the correct format

        This function returns a dataframe from excel data. 

        Params:
            data: This can be a path to a file or a binary object (i.e. a read file).
            sheet_names: This is a list or a singular string representing the name of a sheet in the excel file.

        Returns:
            A pandas dataframe object.
            """
        # Reading in the dataframe with the given sheet name
        df1 = pd.read_excel(data, sheet_name=sheet_names)

        # creating the branch dataframe from a copy of df1
        branch_df = df1.copy()[["Max Branch Flow (gpm)",
                                "Max Branch Diameter (in.)"]]
        # creating a copy of the current index as a new column 'copy_index'
        branch_df.loc[:, 'copy_index'] = branch_df.index
        branch_df["Max Branch Flow (gpm)"] = branch_df["Max Branch Flow (gpm)"].astype(
            float)  # casting the 'Max Branch Flow' to type float
        # Looking in the 'Max Branch Flow' col and removing any rows with a null value
        branch_df.dropna(axis='index', how='any', inplace=True,
                         subset=["Max Branch Flow (gpm)"])

        # creating the header dataframe from a copy of df1
        header_df = df1.copy()[["Max Header Flow (gpm)",
                                "Max Header Diameter (in.)"]]
        # creating a copy of the current index as a new column 'copy_index'
        header_df.loc[:, 'copy_index'] = header_df.index
        header_df["Max Header Flow (gpm)"] = header_df["Max Header Flow (gpm)"].astype(
            float)  # casting the 'Max Header Flow' to type float
        # Looking in the 'Max Header Flow' col and removing any rows with a null value
        header_df.dropna(axis='index', how='any', inplace=True,
                         subset=["Max Header Flow (gpm)"])

        # creating the new dataframe from a copy of df1 with the columns
        reference_df = df1.copy()[["Flow (gpm)", "Pipe Diameter (in.)"]]
        # creating a copy of the current index as a new column 'copy_index'
        reference_df["Flow (gpm)"] = reference_df["Flow (gpm)"].astype(float)
        # Set the dataframe index using the column Flow
        reference_df.set_index("Flow (gpm)", inplace=True)
        # Removing any rows with a null value in any column
        reference_df.dropna(axis='index', how='any', inplace=True)

        branch_output_df = pd.merge_asof(branch_df.sort_values(
            'Max Branch Flow (gpm)'), reference_df, left_on="Max Branch Flow (gpm)", right_on="Flow (gpm)", direction='backward')
        branch_output_df.sort_values(by=['copy_index'], inplace=True)

        header_output_df = pd.merge_asof(header_df.sort_values(
            'Max Header Flow (gpm)'), reference_df, left_on="Max Header Flow (gpm)", right_on="Flow (gpm)", direction='backward')
        header_output_df.sort_values(by=['copy_index'], inplace=True)

        output_df = pd.merge(
            branch_output_df, header_output_df, on="copy_index")
        output_df.drop(['copy_index'], axis=1, inplace=True)

        output_df["Max Branch Diameter (in.)"] = np.where(output_df["Max Branch Diameter (in.)"] ==
                                                          output_df['Pipe Diameter (in.)_x'], output_df["Max Branch Diameter (in.)"], output_df['Pipe Diameter (in.)_x'])
        output_df["Max Header Diameter (in.)"] = np.where(output_df["Max Header Diameter (in.)"] ==
                                                          output_df['Pipe Diameter (in.)_y'], output_df["Max Header Diameter (in.)"], output_df['Pipe Diameter (in.)_y'])
        output_df.drop(columns=['Pipe Diameter (in.)_x',
                       'Pipe Diameter (in.)_y'], inplace=True)

        return output_df

    def write_df_to_excel(df: pd.DataFrame, file_path: FilePath, sheet: str, **kwargs) -> None:
        """This function takes in a dataframe and writes it to the path given by the file path parameter.

        Params:
            df: A pandas dataframe for a given sheet within an excel workbook.
            file_path: A file path to write the dataframe to.
            sheet: The name of the sheet you want to append to.

        Returns:
            It returns nothing.

        This function is a wrapper for the pandas ExcelWriter method in the sense that you can call this function instead of that one."""
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, sheet_name=sheet, index=False, **kwargs)


def group_then_separate_by(psd_data: DataFrame, list_of_cols: list, pn_col: str, str_list: list[str]) -> tuple[DataFrame, DataFrame]:
    """list of cols are grouping categories. pn_col is the column that contains pns to find matches on."""
    psd_data = psd_data.astype({pn_col: str_list.__getitem__(
        0).__class__})  # Converts BOM column into the same datatype as the pn list
    groups = psd_data.groupby(
        list_of_cols)  # Had to play around with this to get the right groupings

    # will hold list of dataframes to be removed. Will concatenate to 1 dataframe later
    df_list_to_remove = []
    # will hold list of dataframes to remain in PSD. Will concatenate to 1 dataframe later
    df_list_to_keep = []

    # Iterates through each sub-group, checking if there is a pn that meets criteria for removal
    for _, frame in groups:
        if any(frame[pn_col].isin(str_list)):   # Finding matching partnumbers to remove
            # Need to add this sub-group to a "removed dataframe"
            df_list_to_remove.append(frame)
        else:
            # Need to retain this sub-group, add to a "keep dataframe"
            df_list_to_keep.append(frame)

    # Concatenating list of dfs to single dfs.
    if len(df_list_to_remove) > 0:
        removals = pd.concat(df_list_to_remove)
    else:
        removals = pd.DataFrame(np.nan, index=[0], columns=psd_data.columns)
    keep = pd.concat(df_list_to_keep)

    return removals, keep


def find_and_replace():
    pass
