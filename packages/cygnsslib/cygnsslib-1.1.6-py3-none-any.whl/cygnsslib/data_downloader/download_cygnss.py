#!/usr/bin/env python3
"""
 DESCRIPTION
          This tool is part of cygnsslib python package. The package is creaded by Mixil lab at USC
          See <https://bitbucket.org/usc_mixil/cygnss-library>

          This Tool download SRTM .hgt data

 AUTHOR   Amer Melebari
          Microwave Systems, Sensors and Imaging Lab (MiXiL)
          University of Southern California
 EMAIL    jamesdca@usc.edu
 CREATED  2020‑07‑19
 Updated  2020-08-22

  Copyright 2020 University of Southern California
"""
from cygnsslib.data_downloader.pass_core import MixilKeys
from getpass import getpass
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from tqdm.auto import tqdm
import datetime as dt
import fnmatch
import numpy as np
import os
import requests
import warnings
from cygnsslib.data_downloader.download_srtm import EarthdataSession

CYG_MIN_FILE_SIZE = 50e6  # in bytes
PODAAC_CYG_URL = 'https://podaac-tools.jpl.nasa.gov/drive/files/allData/cygnss'
L1_VER = 'v2.1'
CHUNK_SIZE = 1024 * 1024  # 1 MB


def download_file(file_url, output_folder, auth=None):
    """
    download the file with url into folder output_folder

    :param file_url: url of the file
    :type file_url: str
    :param output_folder: saving folder
    :type output_folder: str
    :param auth: username or pass
    :type auth: tuple of str or None
    :return: downloaded file path
    :rtype: str
    """

    response = requests.get(file_url, stream=True, auth=auth, allow_redirects=True)
    response.raise_for_status()
    file_name = response.url.split('/')[-1]
    out_file = os.path.join(output_folder, file_name)
    with tqdm.wrapattr(open(out_file, "wb"), "write", miniters=1, total=int(response.headers.get('content-length', 0)), desc=out_file) as fout:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            fout.write(chunk)

    return out_file


def _get_cyg_page_data(cyg_folder_url, podaac_usr_pass):
    with EarthdataSession(username=podaac_usr_pass[0], password=podaac_usr_pass[1]) as session:
        with session.get(cyg_folder_url) as response:
            data = str(response.content).split('<tr>')

    return data


def download_cyg_rawif(data_year, data_day, sc_num, out_folder, podaac_usr_pass, day_page_data=None, download_l1_data=False):
    """
    download cygnss data raw if files from PODAAC, the username and pass can be obtained from https://podaac-tools.jpl.nasa.gov/drive/
    Don't use this function directly, instead use download_cyg_rawif_files()

    :param data_year: data year (ex. 2019)
    :type data_year: int
    :param data_day: data day number (ex. 130)
    :type data_day: int
    :param sc_num: cygnss spacecraft number (1-8)
    :type sc_num: int
    :param out_folder: folder of the saved output (ex: /cygnss_data/L1/v2.1/2019/020)
    :type out_folder: str
    :param podaac_usr_pass: PODAAC user name and pass (usr name, pass)
    :type podaac_usr_pass: tuple of string
    :param day_page_data: page of the selected day, this to reduce the times the script requests the page from the website, default None
    :type day_page_data: list of str or None
    :param download_l1_data: when there is a Rawif data, download its L1 data with it, env $CYGNSS_L1_PATH var should point to the folder of L1 data.
    :type download_l1_data: bool
    :return: file names
    :rtype: list of str
    """
    _files_flag = np.zeros(2).astype(bool)  # check if both the data file and the metadata file are exist
    if not os.path.isdir(out_folder):
        raise ValueError('Invalid out_folder={} specified'.format(out_folder))

    cyg_folder_url = '{:s}/{:s}/{:s}/{:04d}/{:03d}/'.format(PODAAC_CYG_URL, 'L1', 'raw_if', data_year, data_day)
    cyg_files_url = list()
    if day_page_data is None:
        day_page_data = _get_cyg_page_data(cyg_folder_url, podaac_usr_pass)

    tag = 'cyg{:02d}_raw_if'.format(sc_num)
    endtag = '.bin'
    for item in day_page_data:
        if 'cyg' in item:
            try:
                ind = item.index(tag)
                item = item[ind:]
                end = item.index(endtag)
            except ValueError:
                pass
            else:
                file_name = item[:end + 4]
                if 'data' in file_name and not _files_flag[0]:  # only allow one data file name
                    _files_flag[0] = True
                    cyg_files_url.append('{:s}{:s}'.format(cyg_folder_url, file_name))
                elif 'meta' in file_name and not _files_flag[1]:  # only allow one metadata file name
                    _files_flag[1] = True
                    cyg_files_url.append('{:s}{:s}'.format(cyg_folder_url, file_name))

    if not cyg_files_url:  # if no file
        return None
    if not _files_flag.all():  # if only found the data file or the metadata file
        warnings.warn("couldn't find both data and the metadata files for year: {:04d}, day: {:03d}, sc: {:01d}".format(data_year, data_day, sc_num),
                      RuntimeWarning)
    out_files = list()
    for file_url in cyg_files_url:
        out_files.append(download_file(file_url, out_folder, auth=podaac_usr_pass))
    if download_l1_data:
        download_cyg_files(data_year, data_day, sc_num, podaac_usr=podaac_usr_pass[0], podaac_pass=podaac_usr_pass[1])
    return out_files


def download_cyg_file(data_year, data_day, sc_num, cyg_data_ver, cyg_data_lvl, out_folder, podaac_usr_pass, day_page_data=None):
    """
    download cygnss data file from PODAAC, the username and pass can be obtained from https://podaac-tools.jpl.nasa.gov/drive/
    Don't use this function directly, instead use download_cyg_files()

    :param data_year: data year (ex. 2019)
    :type data_year: int
    :param data_day: data day number (ex. 130)
    :type data_day: int
    :param sc_num: cygnss spacecraft number (1-8)
    :type sc_num: int
    :param cyg_data_ver: cygnss data version (ex: 'v2.1')
    :type cyg_data_ver: str
    :param cyg_data_lvl: cygnss data level (ex: 'L1')
    :type cyg_data_lvl: str
    :param out_folder: folder of the saved output (ex: /cygnss_data/L1/v2.1/2019/020)
    :type out_folder: str
    :param podaac_usr_pass: PODAAC user name and pass (usr name, pass)
    :type podaac_usr_pass: tuple of string
    :param day_page_data: page of the selected day, this to reduce the times the script requests the page from the website, default None
    :type day_page_data: list of str or None
    :return: file name
    :rtype: str
    """
    if not os.path.isdir(out_folder):
        raise ValueError('Invalid out_folder={} specified'.format(out_folder))

    cyg_folder_url = '{:s}/{:s}/{:s}/{:04d}/{:03d}/'.format(PODAAC_CYG_URL, cyg_data_lvl, cyg_data_ver, data_year, data_day)
    if day_page_data is None:
        day_page_data = _get_cyg_page_data(cyg_folder_url, podaac_usr_pass)

    tag = 'cyg{:02d}.'.format(sc_num)
    endtag = '.nc'
    for item in day_page_data:
        if 'cyg' in item:
            try:
                ind = item.index(tag)
                item = item[ind:]
                end = item.index(endtag)
            except ValueError:
                pass
            else:
                file_name = item[:end + 3]
                cyg_file_full_url = '{:s}{:s}'.format(cyg_folder_url, file_name)
                download_file(cyg_file_full_url, out_folder, auth=podaac_usr_pass)
                return file_name

    print("File doesn't exist in the PODAAC, year:{:04d}, day:{:03d}, SC: {:02d}".format(data_year, data_day, sc_num))
    return None


def download_rawif_cyg_files_between_date(st_date, end_date, list_sc_num=None, podaac_usr=None, podaac_pass=None, cygnss_l1_path=None,
                                          re_download=False, save_podaac_pass=True, download_l1_data=False):
    """
    download RAWIF CYGNSS data between two dates (including start and end date)

    :param st_date: start date
    :type st_date: date
    :param end_date: end date
    :type end_date: date
    :param list_sc_num: list of cygnss spacecraft numbers (1-8), if None will download all SCs
    :type list_sc_num: list or int or np.array or None
    :param podaac_usr: PODAAC user name. if None, it will ask you to enter it
    :type podaac_usr: str or None
    :param podaac_pass: PODAAC Drive API password. if None, it will ask you to enter it
    :type podaac_pass: str or None
    :param cygnss_l1_path: path of the cygnss L1 data (default: os.environ["CYGNSS_L1_PATH"]), see description for more details
    :type cygnss_l1_path: str or None
    :param re_download: re-download the file if it exist?
    :type re_download: bool
    :param save_podaac_pass: save podaac username and pass in your system? (select False if you're using a shared or public PC)
    :type save_podaac_pass: bool
    :param download_l1_data: when there is a Rawif data, download its L1 data with it, env $CYGNSS_L1_PATH var should point to the folder of L1 data.
    :type download_l1_data: bool
    :return:
    """
    if list_sc_num is None:
        list_sc_num = np.arange(1, 9)
    elif np.size(list_sc_num) == 1:
        list_sc_num = [int(list_sc_num)]

    if cygnss_l1_path is None:
        cygnss_l1_path = os.environ["CYGNSS_L1_PATH"]

    # check if the folder name is not raw_if, if not, change the folder name
    folder_list = cygnss_l1_path.split(os.path.sep)
    if not folder_list[-1]:
        folder_list.pop(-1)
    if 'raw_if' not in folder_list[-1]:
        folder_list[-1] = 'raw_if'
    cygnss_l1_path = os.sep.join(folder_list)

    podaac_usr_pass = get_podaac_cred(save_pass=save_podaac_pass) if (podaac_usr is None or podaac_pass is None) else (podaac_usr, podaac_pass)

    num_days = (end_date - st_date).days + 1
    for iday in range(0, num_days):
        data_date = st_date + dt.timedelta(days=iday)
        data_year = data_date.year
        data_day = (data_date - dt.date(data_year, 1, 1)).days + 1
        _download_single_day_rawif(data_year, data_day, list_sc_num, cygnss_l1_path, podaac_usr_pass, re_download, download_l1_data)


def download_cyg_rawif_files(data_year, list_data_day, list_sc_num=None, podaac_usr=None, podaac_pass=None, cygnss_l1_path=None, re_download=False,
                             save_podaac_pass=True, download_l1_data=False):
    """

    download the raw_if cygnss data,
    if cygnss_l1_path or os.environ["CYGNSS_L1_PATH"]) point to a folder with name not "raw_if", it will save the data in a raw_if folder in the
    parent dir.

    :param data_year: list of data years
    :type data_year:  int
    :param list_data_day: list of data days
    :type list_data_day: list or int or np.array
    :param list_sc_num: list of cygnss spacecraft numbers (1-8), if None will download all SCs
    :type list_sc_num: list or int or np.array or None
    :param podaac_usr: PODAAC user name. if None, it will ask you to enter it
    :type podaac_usr: str or None
    :param podaac_pass: PODAAC Drive API password. if None, it will ask you to enter it
    :type podaac_pass: str or None
    :param cygnss_l1_path: path of the cygnss L1 data (default: os.environ["CYGNSS_L1_PATH"]), see description for more details
    :type cygnss_l1_path: str or None
    :param re_download: re-download the file if it exist?
    :type re_download: bool
    :param save_podaac_pass: save podaac username and pass in your system? (select False if you're using a shared or public PC)
    :type save_podaac_pass: bool
    :param download_l1_data: when there is a Rawif data, download its L1 data with it, env $CYGNSS_L1_PATH var should point to the folder of L1 data.
    :type download_l1_data: bool
    :return:
    """
    if np.size(list_data_day) == 1:
        list_data_day = [int(list_data_day)]
    if list_sc_num is None:
        list_sc_num = np.arange(1, 9)
    elif np.size(list_sc_num) == 1:
        list_sc_num = [int(list_sc_num)]

    if cygnss_l1_path is None:
        cygnss_l1_path = os.environ["CYGNSS_L1_PATH"]

    # check if the folder name is not raw_if, if not, change the folder name
    folder_list = cygnss_l1_path.split(os.path.sep)
    if not folder_list[-1]:
        folder_list.pop(-1)
    if 'raw_if' not in folder_list[-1]:
        folder_list[-1] = 'raw_if'
    cygnss_l1_path = os.sep.join(folder_list)

    podaac_usr_pass = get_podaac_cred(save_pass=save_podaac_pass) if (podaac_usr is None or podaac_pass is None) else (podaac_usr, podaac_pass)

    for data_day in list_data_day:
        _download_single_day_rawif(data_year, data_day, list_sc_num, cygnss_l1_path, podaac_usr_pass, re_download, download_l1_data)


def _download_single_day_rawif(data_year, data_day, list_sc_num, cygnss_l1_path, podaac_usr_pass, re_download, download_l1_data=False):
    """
    download Rawif data for a single day, don't use this function to download the files, instead use download_cyg_rawif_files() or
    download_rawif_cyg_files_between_date ()

    :param data_year: data year
    :type data_year:  int
    :param data_day: data day number
    :type data_day: int
    :param list_sc_num: list of cygnss spacecraft numbers (1-8)
    :type list_sc_num: list or int or np.array
    :param cygnss_l1_path: main path of the data
    :type cygnss_l1_path: str
    :param podaac_usr_pass: PODAAC user name and pass (usr name, pass)
    :type podaac_usr_pass: tuple of string
    :param re_download: re-download the file if it exist?
    :type re_download: bool
    :param download_l1_data: when there is a Rawif data, download its L1 data with it, env $CYGNSS_L1_PATH var should point to the folder of L1 data.
    :type download_l1_data: bool
    :return:
    """
    cyg_day_folder = os.path.join(cygnss_l1_path, '{:04d}'.format(data_year), '{:03d}'.format(data_day))
    cyg_day_folder_url = '{:s}/{:s}/{:s}/{:04d}/{:03d}/'.format(PODAAC_CYG_URL, 'L1', 'raw_if', data_year, data_day)
    day_page_data = _get_cyg_page_data(cyg_day_folder_url, podaac_usr_pass)
    if not os.path.isdir(cyg_day_folder):
        os.makedirs(cyg_day_folder, exist_ok=True)
    for sc_num in list_sc_num:
        cyg_files_name = get_cyg_rawif_files(cyg_day_folder, sc_num)
        if cyg_files_name is None:
            download_cyg_rawif(data_year, data_day, sc_num, cyg_day_folder, podaac_usr_pass=podaac_usr_pass, day_page_data=day_page_data,
                               download_l1_data=download_l1_data)

        elif re_download:
            for file_name in cyg_files_name:
                cyg_file_full_path = os.path.join(cygnss_l1_path, '{:04d}'.format(data_year), '{:03d}'.format(data_day), file_name)
                os.remove(cyg_file_full_path)
            download_cyg_rawif(data_year, data_day, sc_num, cyg_day_folder, podaac_usr_pass=podaac_usr_pass, day_page_data=day_page_data,
                               download_l1_data=download_l1_data)
        else:
            for file_name in cyg_files_name:
                print('{:s} file exist'.format(file_name))


def download_cyg_files(data_year, list_data_day, list_sc_num=None, podaac_usr=None, podaac_pass=None, cyg_data_ver=None, cyg_data_lvl='L1',
                       cygnss_l1_path=None, re_download=False, force_download=False, save_podaac_pass=True):
    """
    
    download multiple CYGNSS files
    
    :param data_year: list of data years
    :type data_year:  int
    :param list_data_day: list of data days
    :type list_data_day: list or int or np.array
    :param list_sc_num: list of cygnss spacecraft numbers (1-8), if None will download all SCs
    :type list_sc_num: list or int or np.array or None
    :param podaac_usr: PODAAC user name. if None, it will ask you to enter it
    :type podaac_usr: str or None
    :param podaac_pass: PODAAC Drive API password. if None, it will ask you to enter it
    :type podaac_pass: str or None
    :param cyg_data_ver: cygnss data version (ex: 'v2.1')
    :type cyg_data_ver: str
    :param cyg_data_lvl: cygnss data level (ex: 'L1')
    :type cyg_data_lvl: str
    :param cygnss_l1_path: path of the cygnss L1 data (default: os.environ["CYGNSS_L1_PATH"])
    :type cygnss_l1_path: str or None
    :param re_download: re-download the file if it exist?
    :type re_download: bool
    :param force_download: re-download the file even if the version is not included in the path (not recommended)
    :type force_download: bool
    :param save_podaac_pass: save podaac username and pass in your system? (select False if you're using a shared or public PC)
    :type save_podaac_pass: bool
    :return: 
    """

    if np.size(list_data_day) == 1:
        list_data_day = [int(list_data_day)]
    if list_sc_num is None:
        list_sc_num = np.arange(1, 9)
    elif np.size(list_sc_num) == 1:
        list_sc_num = [int(list_sc_num)]

    if cygnss_l1_path is None:
        cygnss_l1_path = os.environ["CYGNSS_L1_PATH"]
    cyg_data_ver = L1_VER if cyg_data_ver is None else cyg_data_ver
    cyg_data_lvl = cyg_data_lvl.upper()

    podaac_usr_pass = get_podaac_cred(save_pass=save_podaac_pass) if (podaac_usr is None or podaac_pass is None) else (podaac_usr, podaac_pass)
    ver_folder_exist = check_ver_folder(cygnss_l1_path, cyg_data_ver)
    if not force_download and not ver_folder_exist:
        error_str = "You are trying to download version {:s}, but the path doesn't contain the version name".format(cyg_data_ver)
        raise ValueError('{:s}\nuse force_download=True to remove this error'.format(error_str))

    for data_day in list_data_day:
        _download_cyg_single_day(data_year, data_day, list_sc_num, podaac_usr_pass, cyg_data_ver, cyg_data_lvl, cygnss_l1_path, re_download)


def download_cyg_files_between_date(st_date, end_date, list_sc_num=None, podaac_usr=None, podaac_pass=None, cyg_data_ver=None, cyg_data_lvl='L1',
                                    cygnss_l1_path=None, re_download=False, force_download=False, save_podaac_pass=True):
    """
    download CYGNSS data between two dates (including start and end date)

    :param st_date: start date
    :type st_date: date
    :param end_date: end date
    :type end_date: date
    :param list_sc_num: list of cygnss spacecraft numbers (1-8), if None will download all SCs
    :type list_sc_num: list or np.array or int
    :param podaac_usr: PODAAC user name. if None, it will ask you to enter it
    :type podaac_usr: str or None
    :param podaac_pass: PODAAC Drive API password. if None, it will ask you to enter it
    :type podaac_pass: str or None
    :param cyg_data_ver: cygnss data version (ex: 'v2.1')
    :type cyg_data_ver: str
    :param cyg_data_lvl: cygnss data level (ex: 'L1')
    :type cyg_data_lvl: str
    :param cygnss_l1_path: path of the cygnss L1 data (default: os.environ["CYGNSS_L1_PATH"])
    :type cygnss_l1_path: str or None
    :param re_download: re-download the file if it exist?
    :type re_download: bool
    :param force_download: download the file even if the version is not included in the path (not recommended)
    :param save_podaac_pass: save podaac username and pass in your system? (select False if you're using a shared or public PC)
    :type save_podaac_pass: bool
    :return:
    """

    if list_sc_num is None:
        list_sc_num = np.arange(1, 9)
    elif np.size(list_sc_num) == 1:
        list_sc_num = [int(list_sc_num)]

    if cygnss_l1_path is None:
        cygnss_l1_path = os.environ["CYGNSS_L1_PATH"]
    cyg_data_ver = L1_VER if cyg_data_ver is None else cyg_data_ver
    cyg_data_lvl = cyg_data_lvl.upper()
    podaac_usr_pass = get_podaac_cred(save_pass=save_podaac_pass) if (podaac_usr is None or podaac_pass is None) else (podaac_usr, podaac_pass)

    ver_folder_exist = check_ver_folder(cygnss_l1_path, cyg_data_ver)
    if not force_download and not ver_folder_exist:
        error_str = "You are trying to download version {:s}, but the path doesn't contain the ver name ({:s})".format(cyg_data_ver, cygnss_l1_path)
        raise ValueError('{:s}\nuse force_download=True to remove this error'.format(error_str))

    num_days = (end_date - st_date).days + 1
    for iday in range(0, num_days):
        data_date = st_date + dt.timedelta(days=iday)
        data_year = data_date.year
        data_day = (data_date - dt.date(data_year, 1, 1)).days + 1
        _download_cyg_single_day(data_year, data_day, list_sc_num, podaac_usr_pass, cyg_data_ver, cyg_data_lvl, cygnss_l1_path, re_download)


def _download_cyg_single_day(data_year, data_day, list_sc_num, podaac_usr_pass, cyg_data_ver, cyg_data_lvl, cygnss_l1_path, re_download):
    """
    download a single day, access this function from download_cyg_files()
    :param data_year: data year
    :type data_year: int
    :param data_day: data day of the year
    :type data_day: int
    :param list_sc_num: list of cygnss spacecraft numbers (1-8), if None will download all SCs
    :type list_sc_num: list or np.array or int
    :param podaac_usr_pass: PODAAC user name and pass (usr name, pass)
    :type podaac_usr_pass: tuple of string
    :param cyg_data_ver: cygnss data version (ex: 'v2.1')
    :type cyg_data_ver: str
    :param cyg_data_lvl: cygnss data level (ex: 'L1')
    :type cyg_data_lvl: str
    :param cygnss_l1_path: path of the cygnss L1 data (default: os.environ["CYGNSS_L1_PATH"])
    :type cygnss_l1_path: str
    :param re_download: re-download the file if it exist?
    :type re_download: bool
    :return:
    """
    cyg_day_folder = os.path.join(cygnss_l1_path, '{:04d}'.format(data_year), '{:03d}'.format(data_day))
    if not os.path.isdir(cyg_day_folder):
        os.makedirs(cyg_day_folder, exist_ok=True)
    for sc_num in list_sc_num:
        cyg_file_name = get_cyg_file(cyg_day_folder, sc_num)
        cyg_day_folder_url = '{:s}/{:s}/{:s}/{:04d}/{:03d}/'.format(PODAAC_CYG_URL, cyg_data_lvl, cyg_data_ver, data_year, data_day)
        day_page_data = _get_cyg_page_data(cyg_day_folder_url, podaac_usr_pass)

        if cyg_file_name is None:
            download_cyg_file(data_year, data_day, sc_num, cyg_data_ver, cyg_data_lvl=cyg_data_lvl, out_folder=cyg_day_folder,
                              podaac_usr_pass=podaac_usr_pass, day_page_data=day_page_data)
        else:
            cyg_file_full_path = os.path.join(cygnss_l1_path, '{:04d}'.format(data_year), '{:03d}'.format(data_day), cyg_file_name)
            file_size = os.path.getsize(cyg_file_full_path)
            if re_download:
                os.remove(cyg_file_full_path)
                download_cyg_file(data_year, data_day, sc_num, cyg_data_ver, cyg_data_lvl=cyg_data_lvl, out_folder=cyg_day_folder,
                                  podaac_usr_pass=podaac_usr_pass, day_page_data=day_page_data)
            else:
                if file_size > CYG_MIN_FILE_SIZE:
                    print('{:s} file exist'.format(cyg_file_name))
                else:
                    print('{:s} file size is too small, re-downloading the file')
                    os.remove(cyg_file_full_path)
                    download_cyg_file(data_year, data_day, sc_num, cyg_data_ver, cyg_data_lvl=cyg_data_lvl, out_folder=cyg_day_folder,
                                      podaac_usr_pass=podaac_usr_pass, day_page_data=day_page_data)


def get_cyg_rawif_files(cyg_day_folder, sc_num):
    """
    check if the file exist and return the file name, if not exist return None.
    if exist it will return list of the files

    :param cyg_day_folder: cygnss day folder
    :type cyg_day_folder: str
    :param sc_num: spacescraft number
    :type sc_num: int
    :return: file name
    :rtype: str
    """
    _files_flag = np.zeros(2).astype(bool)
    result = []
    pattern = "cyg{:02d}*.bin".format(sc_num)
    for root, dirs, files in os.walk(cyg_day_folder):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(name)

    if len(result) == 0:
        return None
    else:
        files_name_list = list()
        for file_name in result:
            if 'data' in file_name:
                _files_flag[0] = True
                files_name_list.append(file_name)
            elif 'meta' in file_name:
                _files_flag[1] = True
                files_name_list.append(file_name)

    if not _files_flag.all():
        warnings.warn("couldn't find both data and the metadata files in {:s}, sc: {:d}, try to download both".format(cyg_day_folder, sc_num),
                      RuntimeWarning)
        return None

    return files_name_list


def get_cyg_file(cyg_day_folder, sc_num):
    """
    check if the file exist and return the file name, if not exist return None

    :param cyg_day_folder: cygnss day folder
    :type cyg_day_folder: str
    :param sc_num: spacescraft number
    :type sc_num: int
    :return: file name
    :rtype: str
    """
    result = []
    pattern = "cyg{:02d}*.nc".format(sc_num)
    for root, dirs, files in os.walk(cyg_day_folder):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(name)
                break  # finding the first file

    if len(result) == 0:
        cyg_file_name = None
    else:
        cyg_file_name = result[0]

    return cyg_file_name


def check_ver_folder(cygnss_l1_path, cyg_data_ver):
    """
    check if the version name in the path

    :param cygnss_l1_path: path of the cygnss L1 data (default: os.environ["CYGNSS_L1_PATH"])
    :type cygnss_l1_path: str
    :param cyg_data_ver: cygnss data version (ex: 'v2.1')
    :type cyg_data_ver: str
    :return:
    """
    path_split = cygnss_l1_path.split(os.sep)
    if cyg_data_ver in path_split:
        out = True
    else:
        warnings.warn("You are trying to download version {:s}, but the path doesn't contain the version name".format(cyg_data_ver), RuntimeWarning)
        out = False
    return out


def get_podaac_cred(pass_folder=None, save_pass=True, reset_pass=False):
    """
    import podaac username and pass from the system, if not found it ask you to enter them

    :return:
    """
    if reset_pass:
        mixil_keys = MixilKeys(pass_folder=pass_folder)
        mixil_keys.remove('podaac_usr')
        mixil_keys.remove('podaac_pass')
        del mixil_keys

    print('Get PODAAC API Credentials from: https://podaac-tools.jpl.nasa.gov/drive/')
    if save_pass:
        mixil_keys = MixilKeys(pass_folder=pass_folder)
        mixil_keys.require('podaac_usr', msg='PO.DAAC Username: ')
        mixil_keys.require('podaac_pass', msg='PO.DAAC Drive API Password: ')
        podaac_usr = mixil_keys.retrieve('podaac_usr')
        podaac_pass = mixil_keys.retrieve('podaac_pass')
    else:
        podaac_usr = getpass('PO.DAAC Username: ')
        podaac_pass = getpass('PO.DAAC Drive API Password: ')

    return podaac_usr, podaac_pass


def main():
    podaac_usr, podaac_pass = get_podaac_cred()
    data_day = np.arange(5, 10)
    data_year = 2020
    # sc_num = [3]
    sc_num = None
    re_download = False
    cyg_data_ver = 'v2.1'
    # cygnss_l1_path = os.environ["CYGNSS_L1_PATH"]
    cygnss_l1_path = '/media/amer/Data/cygnss_data/L1/v2.1/'
    download_cyg_files(data_year, data_day, list_sc_num=sc_num, podaac_usr=podaac_usr, podaac_pass=podaac_pass, cyg_data_ver=cyg_data_ver,
                       cyg_data_lvl='L1', cygnss_l1_path=cygnss_l1_path, re_download=re_download)
    st_date = dt.date(year=2019, month=1, day=12)
    end_date = dt.date(year=2020, month=1, day=3)

    download_cyg_files_between_date(st_date, end_date, list_sc_num=sc_num, podaac_usr=podaac_usr, podaac_pass=podaac_pass, cyg_data_ver=cyg_data_ver,
                                    cyg_data_lvl='L1', cygnss_l1_path=cygnss_l1_path, re_download=re_download)

    download_cyg_rawif_files(data_year=2020, list_data_day=227)

    st_date = dt.date(year=2020, month=8, day=4)
    end_date = dt.date(year=2020, month=8, day=4)
    download_rawif_cyg_files_between_date(st_date, end_date)


if __name__ == "__main__":
    main()
