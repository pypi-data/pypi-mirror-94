from functools import partial
from typing import Dict

import numpy as np
import pandas as pd


def stats_per_type_teacher_student_ratio_per_district(data: pd.DataFrame) -> pd.DataFrame:
    data["S/T"] = data["Uczniowie, wychow., słuchacze"] / data["Nauczyciele"]
    data_grouped = data.groupby(["Nazwa typu", "Gmina"]).agg(
        {"S/T": ["min", "max", "mean"]})
    return data_grouped


def students_rural_area(row, data_inhabitants):
    if row["Typ gminy"] == "M-Gm":
        rows_inhabitants = data_inhabitants[row["Województwo"]].loc[
            (data_inhabitants[row["Województwo"]]["Id"] == row["Id"]) & (
                    data_inhabitants[row["Województwo"]]["Wyszczególnienie"] == "   Edukacyjne grupy wieku     ")]
        percent_of_rural = rows_inhabitants["Wieś razem"].iloc[0] / rows_inhabitants["Ogółem"].iloc[0]
        return round(row["Uczniowie, wychow., słuchacze"] * percent_of_rural)
    elif row["Typ gminy"] == "Gm":
        return row["Uczniowie, wychow., słuchacze"]
    return 0


def stats_per_type_teacher_student_ratio_per_district_type(data_school: pd.DataFrame,
                                                           data_inhabitants: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    partial_replace = partial(students_rural_area, data_inhabitants=data_inhabitants)
    data_school["Uczniowie_w"] = data_school.apply(lambda x: partial_replace(x), axis=1)
    data_school = data_school.assign(
        Uczniowie_m=data_school["Uczniowie, wychow., słuchacze"] - data_school["Uczniowie_w"])

    data_school["S_W/T"] = data_school["Uczniowie_w"] / data_school["Nauczyciele"]
    data_school["S_M/T"] = data_school["Uczniowie_m"] / data_school["Nauczyciele"]
    data_grouped = data_school.groupby(["Nazwa typu"]).agg(
        {"S_W/T": ["min", "max", "mean"],
         "S_M/T": ["min", "max", "mean"]
         })
    return data_grouped


# only for 5 main types of school 

dict_school = {"Przedszkole": [3, 6, "      3- 6   lat              "],
               "Szkoła podstawowa": [7, 12, "      7-12   lat              "],
               "Gimnazjum": [13, 15, "     13-15   lat              "],
               "Liceum ogólnokształcące": [16, 18, "     16-18   lat              "],
               "Szkoła policealna": [19, 24, "     19-24   lat              "]}


def select_num_stud_by_id_spec(dict_df, row, specification, col_name):
    res = dict_df[row["Województwo"]].loc[(dict_df[row["Województwo"]]["Id"] == row["Id"]) & (
            dict_df[row["Województwo"]]["Wyszczególnienie"] == specification)][col_name]
    if not res.empty:
        return res.iloc[0]
    return np.nan


def stats_per_year(data_school: pd.DataFrame, data_inhabitants: Dict[str, pd.DataFrame]):
    district = []
    s_year = []
    students = []

    for index, row in data_school.iterrows():
        if row["Nazwa typu"] in dict_school:
            total_student_years = select_num_stud_by_id_spec(data_inhabitants, row, dict_school[row["Nazwa typu"]][2],
                                                             "Ogółem")
            for year in range(dict_school[row["Nazwa typu"]][0], dict_school[row["Nazwa typu"]][1] + 1):
                total_student_year = select_num_stud_by_id_spec(data_inhabitants, row,
                                                                f"       {year if len(str(year)) > 1 else str(year) + ' '}",
                                                                "Ogółem")
                percent_students = total_student_year / total_student_years
                students.append(percent_students * row["Uczniowie, wychow., słuchacze"])
                district.append(row["Gmina"])
                s_year.append(2018 - year)
    students_per_year = pd.DataFrame({"Gmina": district, "Rok urodzenia": s_year, "Uczniowie": students})
    data_grouped = students_per_year.groupby(["Gmina", "Rok urodzenia"]).agg({"Uczniowie": ["min", "max", "mean"]})
    return data_grouped


def stats_per_year_district_type(data_school: pd.DataFrame, data_inhabitants: Dict[str, pd.DataFrame]):
    district = []
    s_year = []
    students = []
    for index, row in data_school.iterrows():
        if row["Nazwa typu"] in dict_school:
            total_student_years = select_num_stud_by_id_spec(data_inhabitants, row, dict_school[row["Nazwa typu"]][2],
                                                             "Ogółem")
            for year in range(dict_school[row["Nazwa typu"]][0], dict_school[row["Nazwa typu"]][1] + 1):
                for area_type in ['Miasta razem', 'Wieś razem']:
                    total_student_year = select_num_stud_by_id_spec(data_inhabitants, row,
                                                                    f"       {year if len(str(year)) > 1 else str(year) + ' '}",
                                                                    area_type)
                    if str(total_student_year).isdigit():  # add only if area has students
                        percent_students = total_student_year / total_student_years
                        students.append(percent_students * row["Uczniowie, wychow., słuchacze"])
                        district.append(area_type.split(' ')[0])
                        s_year.append(2018 - year)
    students_per_year = pd.DataFrame({"Typ obszaru": district, "Rok urodzenia": s_year, "Uczniowie": students})
    data_grouped = students_per_year.groupby(["Typ obszaru", "Rok urodzenia"]).agg(
        {"Uczniowie": ["min", "max", "mean"]})
    return data_grouped
