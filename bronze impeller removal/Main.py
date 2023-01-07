import time
from utils import add_function_to_task,multi_PSD,get_files_in_dir,group_then_separate_by,process_dir,write_new_PSD

if __name__ == '__main__':

    ##### INPUTS #######
    MYDIR= r"C:\Projects\2022\Michaels_Code\grundfos-express-tools\bronze impeller removal\input files"
    target_dir=r'C:\Projects\2022\Michaels_Code\grundfos-express-tools\bronze impeller removal\output files'

    list_of_pns = [
        91842453,
        96823614,
        91842349,
        96866173,
        91841824,
        96823595,
        91841817,
        96823593,
        96823473,
        96866185,
        96866195,
        91842531,
        96823612,
        91842576,
        96866184,
        91841828,
        91841836,
        96866172,
        91840997,
        91841750,
        96823587,
        91841757,
        96823588,
        91842551,
        96823594,
        91842557,
        91841720,
        96823582,
        91841726,
        96823583,
        91842487,
        96823618,
        91842511,
        91841530,
        96823535,
        91841526,
        91841685,
        91841690,
        96823564,
        96866856,
        91841736,
        96823585,
        91841767,
        96823590,
        91841764,
        96866853,
        91841713,
        96823581,
        91841707,
        96823580,
        91841786,
        96866190,
        91841657,
        96823538
    ]
#     list_of_pns=[98876008,
# 98876012]

    str_list = [str(numstr) for numstr in list_of_pns]

    #Only want to add an Impeller Sheet 
    sheet_list=[]
    sheet='Case'

    for file in get_files_in_dir(MYDIR,('.xlsx')):
        sheet_list.append([sheet])
    
    tasks=process_dir(MYDIR,sheet_list,target_dir,False)
    add_function_to_task(tasks,group_then_separate_by,["Model", "Price ID"] ,"BOM",str_list=str_list)
    
    multi_PSD(tasks,write_new_PSD)
