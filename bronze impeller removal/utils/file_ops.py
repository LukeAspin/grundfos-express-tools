import datetime
import os
from os import walk
from _types._types import *


def add_str_to_filename(filepath_to_copy: str,strng) -> str:
    """ Appends a string to the file name. """
    _, filename = os.path.split(filepath_to_copy) # Splits filepath to folder, file
    working_copy = strng + " " + filename # adds timestamp to filename
    return(working_copy)

def get_files_in_dir(dir:FolderPath,extension:list[str]|str|None=None):
    arr=[]
    filenames = next(walk(dir), (None, None, []))[2]
    if extension:
        for file in filenames:
            if file.endswith((extension)):
                arr.append(file)
    else:
        arr=filenames
    return arr



def read_files_in_dir(dir:FolderPath)->Generator[Callable,None,None]:
    """Iterates over a given directory
    
    Params:
        dir: A directory 
        
    Returns a generator object that calls a read from file method. 
    """
    filenames = next(walk(dir), (None, None, []))[2]
    for file in filenames:
        _file=os.path.join(dir, file)
        yield read_single_file(_file)



def read_single_file(file:FilePath,chunksize:bytes=1024,is_pool_ready:bool=False)->tuple[bytes,str]:
    f"""This method read in a file by a given chunk size.
        Params:
        file: This is a file like object with supports read, write, and append operations.
        chunksize: The number of bytes to read in at a time (This is more for the multi-processing/multi-threading process)

        Flags:
        [NOT IMPLEMENTED] is_pool_ready: This parameter is used to set the mode of the function. If set to True it is initalized to run with threading/multiprocessing.

        Defaults:
        chunksize = 1024 bytes
        is_bool_ready=False

        Returns:
        (data,file) : The return is a tuple of the files binary data in bytes and the file object.  
        """
    if is_pool_ready:
        print('NOT IMPLEMENTED')
    else:
        res=b''
        with open(file,'rb') as f2:
            while True:
                data=f2.read(chunksize)
                if not data:
                    break
                res+=data
            return res,file



def add_filename_timestamp(filepath_to_copy: str) -> str:
    """ Creates a working copy of the file. Useful when performing changes to an excel spreadsheet and wanting to keep original file unchanged"""
    dir, filename = os.path.split(filepath_to_copy) # Splits filepath to folder, file
    timeStamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    working_copy = timeStamp + " " + filename # adds timestamp to filename
    working_copy = os.path.join(dir, working_copy) # concats to new filepath
    return(working_copy)

def batchRenameAppend(myDir, appendString):
    """ This function appends a string to all the files within the directory """
    for root, subdirectories, files in os.walk(myDir):             # Goes through all dir, subdir to find new schematic pdfs
        for file in files:
            pathname, extension = os.path.splitext(file)
            newFilename = pathname + appendString                                         # Strips file type extension 
            originalFilename = os.path.join(root, pathname + extension)
            newFilename = os.path.join(root, newFilename + extension)
            os.rename(originalFilename, newFilename)
    return

def iterateSubDirFiles(workingDirectory, *extraFunctions):
    """ Iterates through all files within a directory and perform function on each file"""
    for root, subdirectories, files in os.walk(workingDirectory):
        for file in files:
            # fileName, fileExtension = os.path.splitext(file)
            fileName = os.path.join(workingDirectory, file)
            print("Opening file for updates: {}".format(fileName))
            if len(extraFunctions) > 0:
                functionForFile = extraFunctions[0]
                functionForFile(fileName)
    return
###############################################################################