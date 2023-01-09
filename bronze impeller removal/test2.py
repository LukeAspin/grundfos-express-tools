import pandas as pd
from utils.Dataframe_tools import PSD
from utils import add_function_to_task, process_dir, multi_PSD, write_new_PSD


def find_and_replace(df: pd.DataFrame, to_replace, new_value) -> None:
    df.replace(to_replace=to_replace, value=new_value,
               regex=True, inplace=True)


if __name__ == '__main__':

    # MYDIR = r"C:\Projects\2022\Michaels_Code\grundfos-express-tools\bronze impeller removal\input files"
    # target_dir = r'C:\Projects\2022\Michaels_Code\grundfos-express-tools\bronze impeller removal\output files'

    # # Setting the Values
    # IO = 'input files\KPBom.xlsx'

    # find_remove = [{
    #     '91840054': '99717392',
    #     '91840056': '99717485',
    #     '98441969': '92758523',
    #     '96698939': '92758528',     # in KPbom.xlsx
    #     '96698968': '92758121',     # in KPbom.xlsx
    #     '96768950': '92758767',     # in KPbom.xlsx
    #     '99413027': '92758120',
    #     '1020-3/4': '1020-5/6',
    #     '1020-3_4': '1020-5_6',
    #     'Desc-1020-3_4-KP_4': 'Desc-1020-5_6-KP_6',
    #     'Desc-1020-3_4-KP_3': 'Desc-1020-5_6-KP_5'
    # }, ]

    # tasks = process_dir(MYDIR, [['Case']], target_dir, False)
    # add_function_to_task(tasks, find_and_replace, list(
    #     find_remove[0].keys()), list(find_remove[0].values()))
    # multi_PSD(tasks, find_and_replace)
