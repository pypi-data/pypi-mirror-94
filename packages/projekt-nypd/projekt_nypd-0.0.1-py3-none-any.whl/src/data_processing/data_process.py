import logging
from functools import partial
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def _check_file(file):
    if not Path(file).is_file():
        logging.error("File does not exist...")
        raise FileExistsError
    if True not in [str(file).endswith(ending) for ending in ["xls", "xlsx", "xlsm", "xlsb", "odf", "ods", "odt"]]:
        logging.error("Expected excel file type...")
        raise Exception


def load_school_file(file_name) -> pd.DataFrame:
    _check_file(file_name)
    school_data = pd.read_excel(file_name, "Identyfikacja",
                                usecols=["Nazwa typu",
                                         "Typ gminy",
                                         "woj",
                                         "pow",
                                         "gm",
                                         "Województwo",
                                         "Gmina",
                                         "Nazwa szkoły, placówki",
                                         "Regon jednostki sprawozdawczej",
                                         "Regon",
                                         "Uczniowie, wychow., słuchacze",
                                         "Nauczyciele pełnozatrudnieni",
                                         "Nauczyciele niepełnozatrudnieni (stos.pracy)"])
    school_data = school_data.iloc[1:]
    school_data["Województwo"] = school_data["Województwo"].str.replace('WOJ. ', '').str.capitalize()
    school_data["Nauczyciele"] = school_data[["Nauczyciele pełnozatrudnieni",
                                              "Nauczyciele niepełnozatrudnieni (stos.pracy)"]].agg(sum, axis=1)
    school_data["Id"] = school_data["woj"].apply(_float_id_to_str) + school_data["pow"].apply(_float_id_to_str) + \
                        school_data["gm"].apply(_float_id_to_str)
    school_data.drop(["Nauczyciele pełnozatrudnieni", "Nauczyciele niepełnozatrudnieni (stos.pracy)", "woj", "pow",
                      "gm"], axis=1, inplace=True)
    logging.info(f"Loaded data from file {file_name}...")
    return school_data


def _float_id_to_str(num: float):
    return ('0' + str(int(num)))[-2:]


def filter_schools_without_students_and_teacher(school_data: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    data_zero = school_data.loc[(school_data["Nauczyciele"] == 0) & (school_data["Uczniowie, wychow., słuchacze"] == 0)]
    data_non_zero = school_data.loc[~((school_data["Nauczyciele"] == 0) &
                                      (school_data["Uczniowie, wychow., słuchacze"] == 0))]
    logging.info(f"Rows with zeros: {data_zero.shape[0]}, rows without zeros: {data_non_zero.shape[0]} "
                 f"in both students and teachers...")
    return data_non_zero, data_zero


def filter_schools_without_teachers(school_data: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    data_zero = school_data.loc[school_data["Nauczyciele"] == 0]
    data_non_zero = school_data.loc[~((school_data["Nauczyciele"] == 0))]
    logging.info(f"Rows with zeros: {data_zero.shape[0]}, rows without zeros: {data_non_zero.shape[0]} "
                 f"in teachers...")
    return data_non_zero, data_zero


def replace_teachers_num(row, data):
    if row["Nauczyciele"] == 0:
        a = data.loc[data["Regon"] == row["Regon jednostki sprawozdawczej"]]["Nauczyciele"].values
        return a[0]
    return row["Nauczyciele"]


def correct_schools_with_missing_teachers(school_data: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    partial_replace = partial(replace_teachers_num, data=school_data)
    teachers = school_data.apply(partial_replace, axis=1)
    school_data = school_data.assign(Nauczyciele=teachers.values)
    data_non_zero, data_zero = filter_schools_without_teachers(school_data)
    logging.info(f"Final shape of data without zeros in teachers: {data_non_zero.shape}...")
    return data_non_zero, data_zero


def load_and_process_school_file(file_name) -> pd.DataFrame:
    school_data = load_school_file(file_name)
    school_data, zeros_stud_teach = filter_schools_without_students_and_teacher(school_data)
    school_data_corrected, zeros_teachers = correct_schools_with_missing_teachers(school_data)
    return school_data_corrected


def load_inhabitants_file(file_name) -> Dict[str, pd.DataFrame]:
    _check_file(file_name)
    sheet_to_df_map = pd.read_excel(file_name, sheet_name=None, skiprows=5, header=[0, 1])
    logging.info(f"Loaded data file {file_name} ...")
    return sheet_to_df_map


def _replace_col_name_inhabitants(name):
    if len(name[1].replace("  ", "\n").split("\n")) > 1:
        return name[0].replace("  ", "\n").split("\n")[0].strip() + " " + name[1].replace("  ", "\n").split("\n")[
            0].strip()
    return name[0].replace("  ", "\n").split("\n")[0].strip()


def rename_columns_inhabitants(df_dict: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    for df_name in df_dict:
        df_dict[df_name].columns = map(_replace_col_name_inhabitants, df_dict[df_name].columns)
    logging.info("Renamed columns...")
    return df_dict


def fill_missing_id_values_inhabitants(df_dict: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    for df_name in df_dict:
        df_dict[df_name].replace('       ', np.nan, inplace=True)
        df_dict[df_name].fillna(method='ffill', inplace=True)
        df_dict[df_name]['Identyfikator terytorialny'] = df_dict[df_name]['Identyfikator terytorialny'].apply(
            lambda x: ('0' + str(int(x)))[-7:])
        df_dict[df_name]['Id'] = df_dict[df_name]['Identyfikator terytorialny'].str[:-1]
        df_dict[df_name]['Id rodzaj'] = df_dict[df_name]['Identyfikator terytorialny'].str[-1:]
        df_dict[df_name].drop(["Identyfikator terytorialny"], axis=1, inplace=True)
    logging.info("Filled missing ids...")
    return df_dict


def load_and_process_inhabitants(file: str) -> Dict[str, pd.DataFrame]:
    df_dict = load_inhabitants_file(file)
    df_dict = rename_columns_inhabitants(df_dict)
    df_dict = fill_missing_id_values_inhabitants(df_dict)
    return df_dict
