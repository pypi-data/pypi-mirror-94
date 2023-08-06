import numpy as np
import pandas as pd
import pytest

from src.data_statistics.data_stats_for_school import stats_per_type_teacher_student_ratio_per_district, \
    students_rural_area, stats_per_type_teacher_student_ratio_per_district_type, select_num_stud_by_id_spec, \
    stats_per_year, stats_per_year_district_type


def test_stats_per_type_teacher_student_ratio_per_district():
    df = pd.DataFrame({"Nazwa typu": ["1", "1", "2", "1"],
                       "Gmina": ["a", "b", "a", "b"],
                       "Uczniowie, wychow., słuchacze": [10, 20, 15, 30],
                       "Nauczyciele": [100, 100, 100, 100]
                       })
    result = stats_per_type_teacher_student_ratio_per_district(df)
    assert result.shape == (3, 3)
    assert ("S/T", "min") in result
    assert ("S/T", "max") in result
    assert ("S/T", "mean") in result
    assert ("1", "a") in result.index
    assert ("1", "b") in result.index
    assert ("2", "a") in result.index
    assert result.loc[("1", "a")].values.tolist() == [0.1, 0.1, 0.1]
    assert result.loc[("1", "b")].values.tolist() == [0.2, 0.3, 0.25]
    assert result.loc[("2", "a")].values.tolist() == [0.15, 0.15, 0.15]


@pytest.mark.parametrize("row, expected", [
    (pd.Series({"Typ gminy": "M-Gm", "Województwo": "df", "Id": 1, "Uczniowie, wychow., słuchacze": 30},
               index=["Typ gminy", "Województwo", "Id", "Uczniowie, wychow., słuchacze"]), 15),
    (pd.Series({"Typ gminy": "M-Gm", "Województwo": "df", "Id": 2, "Uczniowie, wychow., słuchacze": 45},
               index=["Typ gminy", "Województwo", "Id", "Uczniowie, wychow., słuchacze"]), 4),
    (pd.Series({"Typ gminy": "M", "Województwo": "df", "Id": 4, "Uczniowie, wychow., słuchacze": 60},
               index=["Typ gminy", "Województwo", "Id", "Uczniowie, wychow., słuchacze"]), 0),
    (pd.Series({"Typ gminy": "Gm", "Województwo": "df", "Id": 3, "Uczniowie, wychow., słuchacze": 2},
               index=["Typ gminy", "Województwo", "Id", "Uczniowie, wychow., słuchacze"]), 2)])
def test_students_rural_area(row, expected):
    df_dict = {"df": pd.DataFrame({"Id": [1, 2, 3, 4],
                                   "Wyszczególnienie": ["   Edukacyjne grupy wieku     ",
                                                        "   Edukacyjne grupy wieku     ",
                                                        "   Edukacyjne grupy wieku     ",
                                                        "   Edukacyjne grupy wieku     "],
                                   "Wieś razem": [50, 20, 100, 0],
                                   "Ogółem": [100, 200, 100, 600]
                                   })}
    result = students_rural_area(row, df_dict)
    assert result == expected


def test_stats_per_type_teacher_student_ratio_per_district_type():
    data_school = pd.DataFrame({"Typ gminy": ["M-Gm", "M"],
                                "Nazwa typu": ["1", "2"],
                                "Województwo": ["df", "df"],
                                "Id": [1, 2],
                                "Uczniowie, wychow., słuchacze": [30, 100],
                                "Nauczyciele": [10, 20]})
    df_dict = {"df": pd.DataFrame({"Id": [1, 2],
                                   "Wyszczególnienie": ["   Edukacyjne grupy wieku     ",
                                                        "   Edukacyjne grupy wieku     "],
                                   "Wieś razem": [50, 0],
                                   "Ogółem": [100, 2000]
                                   })}
    result = stats_per_type_teacher_student_ratio_per_district_type(data_school, df_dict)
    assert result.shape == (2, 6)
    assert result.loc["1"].values.tolist() == [1.5, 1.5, 1.5, 1.5, 1.5, 1.5]
    assert result.loc["2"].values.tolist() == [0.0, 0.0, 0.0, 5.0, 5.0, 5.0]


@pytest.mark.parametrize("row, expected", [(pd.Series({"Województwo": "w", "Id": 10}, index=["Województwo", "Id"]), 10),
                                           (pd.Series({"Województwo": "w", "Id": 1}, index=["Województwo", "Id"]),
                                            np.nan)])
def test_select_num_stud_by_id_spec(row, expected):
    df_dict = {"w": pd.DataFrame({"Id": [10, 15], "Wyszczególnienie": ["Razem", "Wieś"], "col": [10, 12]})}
    result = select_num_stud_by_id_spec(df_dict, row, "Razem", "col")
    if np.isnan(expected):
        assert np.isnan(result)
    else:
        assert result == expected


def create_data_school():
    return pd.DataFrame({"Typ gminy": ["M-Gm", "M"],
                         "Gmina": ["1", "2"],
                         "Nazwa typu": ["Przedszkole", "Gimnazjum"],
                         "Województwo": ["df", "df"],
                         "Id": [1, 2],
                         "Uczniowie, wychow., słuchacze": [30, 100],
                         })


def create_df_dict():
    return {"df": pd.DataFrame({"Id": [1] * 5 + [2] * 4,
                                "Wyszczególnienie": ["       3 ",
                                                     "       4 ", "       5 ", "       6 ",
                                                     "      3- 6   lat              ",
                                                     "     13-15   lat              ",
                                                     "       13", "       14", "       15"],
                                "Wieś razem": [10, 20, 30, 40, 100, 0, 0, 0, 0],
                                "Miasta razem": [10, 20, 30, 40, 100, 100, 30, 10, 60],
                                "Ogółem": [20, 40, 60, 80, 200, 100, 30, 10, 60],
                                })}


def test_stats_per_year():
    data_school = create_data_school()
    df_dict = create_df_dict()
    result = stats_per_year(data_school, df_dict)
    assert result.shape == (7, 3)
    assert result.loc[("1", 2012)].values.tolist() == [12.0, 12.0, 12.0]
    assert result.loc[("1", 2013)].values.tolist() == [9.0, 9.0, 9.0]
    assert result.loc[("1", 2014)].values.tolist() == [6.0, 6.0, 6.0]
    assert result.loc[("1", 2015)].values.tolist() == [3.0, 3.0, 3.0]
    assert result.loc[("2", 2003)].values.tolist() == [60.0, 60.0, 60.0]
    assert result.loc[("2", 2004)].values.tolist() == [10.0, 10.0, 10.0]
    assert result.loc[("2", 2005)].values.tolist() == [30.0, 30.0, 30.0]


def test_stats_per_year_district_type():
    data_school = create_data_school()
    df_dict = create_df_dict()
    result = stats_per_year_district_type(data_school, df_dict)
    assert result.shape == (14, 3)
    assert result.loc[("Miasta", 2003)].values.tolist() == [60.0, 60.0, 60.0]
    assert result.loc[("Miasta", 2004)].values.tolist() == [10.0, 10.0, 10.0]
    assert result.loc[("Miasta", 2005)].values.tolist() == [30.0, 30.0, 30.0]
    assert result.loc[("Miasta", 2014)].values.tolist() == [3.0, 3.0, 3.0]
    assert result.loc[("Wieś", 2005)].values.tolist() == [0.0, 0.0, 0.0]
    assert result.loc[("Wieś", 2014)].values.tolist() == [3.0, 3.0, 3.0]
