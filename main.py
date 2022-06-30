#!/user/bin/env python3
# encoding utf-8
"""
main.py - example of a Python 3 application
"""
import argparse
import sys
import time
import multiprocessing
from pathlib import Path
import boto3


def parse_sys_args(sys_args: list) -> argparse:
    """
    Use argparse to process any commandline arguments that were
    passed into the python file.
    Also enable '-h' argument for users that prefer a cli feel
    :param sys_args: list of command line arguments
    :return: argparse object
    """
    parser = argparse.ArgumentParser(description="Example Python 3 Program")

    parser.add_argument("--name", "-n", type=str, help="Person's name")

    parser.add_argument("--file", "-f", type=str, help="Complete path to file to upload and try to download")

    return parser.parse_args(sys_args)


def print_hi(name: str):
    print(f'Hi, {name}')


def main(sys_args: list) -> int:
    """
    Entry function
    :param sys_args: list of strings passed after the python file name
    :return: 0 if successful run or 1 if failure
    """
    response = 1

    try:
        arguments = parse_sys_args(sys_args)
        if not arguments.name:
            print('A --name argument must be provided to this program which is the name of the user running '
                  'this program')
            return response
        if not arguments.file:
            print('A --file argument must be provided to this program which is the complete path to the file to '
                  'upload and try to download')
            return response

        print_hi(arguments.name)
        print(f'Going to upload {arguments.file} in one thread and try to download it in another thread while '
              f'file is being uploaded.')

        p_upload = multiprocessing.Process(target=upload_boto3, args=(arguments.file,))
        p_upload.start()

        p_download = multiprocessing.Process(target=download_boto3, args=(arguments.file,))
        p_download.start()

        p_upload.join()
        p_download.join()

        return 0

    except ValueError as e:
        print(f'Unable to continue: {e}')
        return response


def upload_boto3(upload_file):
    curr_proc = multiprocessing.current_process()
    print(f'Starting upload of {upload_file} in {curr_proc}')
    s3 = boto3.client('s3')
    s3.upload_file(upload_file, "stfm-conference-media", "testfolder/3137_Sullivan_Erika.wmv")
    print(f'File uploaded FINISHED in {curr_proc}')


def download_boto3(download_file):
    filename = Path(download_file)
    curr_proc = multiprocessing.current_process()
    downloaded_file = False
    print("Waiting 5 seconds to do first download attempt...")
    time.sleep(5)
    count = 1
    while not downloaded_file:
        try:
            print(f'Download attempt {count} in {curr_proc}')
            s3 = boto3.client('s3')
            s3.download_file("stfm-conference-media", "testfolder/3137_Sullivan_Erika.wmv",
                             filename.name + ".copy")
            print(f'File DOWNLOADED in {curr_proc}')
            downloaded_file = True
        except Exception as e:
            print(f'File {filename.name} not available in {curr_proc} - {e}')
            time.sleep(1)
            count = count + 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
