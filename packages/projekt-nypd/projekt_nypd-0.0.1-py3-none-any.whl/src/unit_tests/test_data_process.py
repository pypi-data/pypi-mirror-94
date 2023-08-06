import pytest
import pandas as pd

from src.data_processing.data_process import load_school_file, filter_schools_without_students_and_teacher, \
    filter_schools_without_teachers, replace_teachers_num, correct_schools_with_missing_teachers, load_inhabitants_file, \
    rename_columns_inhabitants, fill_missing_id_values_inhabitants


def test_load_school_file_exist_error():
    with pytest.raises(FileExistsError):
        load_school_file("../../data")


def test_load_school_file_wrong_file_type():
    with pytest.raises(Exception):
        load_school_file("../../data/profiler_results/data_process.png")


@pytest.fixture(scope='session')
def excel_file(tmpdir_factory):
    df = pd.DataFrame({"Nazwa typu": ["Szkoła", "LO"],
                       "Typ gminy": ["M", "W"],
                       "woj": ["01", "12"],
                       "pow": ["12", "13"],
                       "gm": ["34", "01"],
                       "Województwo": ["m.st W", "WOJ. województwo"],
                       "Gmina": ["G", "gmina"],
                       "Nazwa szkoły, placówki": ["Szkoła nr 107", "LO 1"],
                       "Regon jednostki sprawozdawczej": ["107890", "107890"],
                       "Regon": ["107890", "109990"],
                       "Uczniowie, wychow., słuchacze": [14, 0],
                       "Nauczyciele pełnozatrudnieni": [2, 1],
                       "Nauczyciele niepełnozatrudnieni (stos.pracy)": [1, 0]})
    filename = str(tmpdir_factory.mktemp('data').join('data.xlsx'))
    df.to_excel(filename, sheet_name='Identyfikacja', index=False)
    return filename


def test_load_school_file(excel_file):
    school_data = load_school_file(excel_file)
    assert "Id" in school_data
    assert "Nauczyciele" in school_data
    assert school_data.shape == (1, 10)
    assert school_data.loc[1, "Województwo"] == "Województwo"


@pytest.mark.parametrize("df, expected1, expected2",
                         [(pd.DataFrame({"Nauczyciele": [0., 0., 0.], "Uczniowie, wychow., słuchacze": [0., 0., 0.]}),
                           pd.DataFrame({"Nauczyciele": [], "Uczniowie, wychow., słuchacze": []}),
                           pd.DataFrame({"Nauczyciele": [0., 0., 0.], "Uczniowie, wychow., słuchacze": [0., 0., 0.]})),
                          (pd.DataFrame({"Nauczyciele": [0., 10., 10.], "Uczniowie, wychow., słuchacze": [0., 1., 6.]}),
                           pd.DataFrame({"Nauczyciele": [10., 10.], "Uczniowie, wychow., słuchacze": [1., 6., ]}),
                           pd.DataFrame({"Nauczyciele": [0.], "Uczniowie, wychow., słuchacze": [0.]})),
                          (
                                  pd.DataFrame(
                                      {"Nauczyciele": [10., 20., 30.], "Uczniowie, wychow., słuchacze": [1., 2., 3.]}),
                                  pd.DataFrame(
                                      {"Nauczyciele": [10., 20., 30.], "Uczniowie, wychow., słuchacze": [1., 2., 3.]}),
                                  pd.DataFrame({"Nauczyciele": [], "Uczniowie, wychow., słuchacze": []})),
                          ])
def test_filter_schools_without_students_and_teacher(df, expected1, expected2):
    res1, res2 = filter_schools_without_students_and_teacher(df)
    assert res1.shape == expected1.shape
    assert res2.shape == expected2.shape


@pytest.mark.parametrize("df, expected1, expected2",
                         [(pd.DataFrame({"Nauczyciele": [0., 0., 0.], "Uczniowie, wychow., słuchacze": [0., 0., 0.]}),
                           pd.DataFrame({"Nauczyciele": [], "Uczniowie, wychow., słuchacze": []}),
                           pd.DataFrame({"Nauczyciele": [0., 0., 0.], "Uczniowie, wychow., słuchacze": [0., 0., 0.]})),
                          (
                                  pd.DataFrame(
                                      {"Nauczyciele": [0., 10., 10.], "Uczniowie, wychow., słuchacze": [10., 1., 6.]}),
                                  pd.DataFrame(
                                      {"Nauczyciele": [10., 10.], "Uczniowie, wychow., słuchacze": [1., 6., ]}),
                                  pd.DataFrame({"Nauczyciele": [0.], "Uczniowie, wychow., słuchacze": [10.]})),
                          (
                                  pd.DataFrame(
                                      {"Nauczyciele": [10., 20., 30.], "Uczniowie, wychow., słuchacze": [1., 0., 3.]}),
                                  pd.DataFrame(
                                      {"Nauczyciele": [10., 20., 30.], "Uczniowie, wychow., słuchacze": [1., 0., 3.]}),
                                  pd.DataFrame({"Nauczyciele": [], "Uczniowie, wychow., słuchacze": []})),
                          ])
def test_filter_schools_without_teachers(df, expected1, expected2):
    res1, res2 = filter_schools_without_teachers(df)
    assert res1.shape == expected1.shape
    assert res2.shape == expected2.shape


@pytest.mark.parametrize("df,row, expected",
                         [(pd.DataFrame({"Nauczyciele": [38], "Regon": [10]}),
                           pd.Series({"Nauczyciele": 0, "Regon jednostki sprawozdawczej": 10},
                                     index=['Nauczyciele', 'Regon jednostki sprawozdawczej']), 38),
                          (pd.DataFrame({"Nauczyciele": [38], "Regon": [10]}),
                           pd.Series({"Nauczyciele": 11, "Regon jednostki sprawozdawczej": 10},
                                     index=['Nauczyciele', 'Regon jednostki sprawozdawczej']), 11),
                          ])
def test_replace_teachers_num(df, row, expected):
    result = replace_teachers_num(row, df)
    assert result == expected


@pytest.mark.parametrize("df, expected1, expected2",
                         [(pd.DataFrame({"Nauczyciele": [0., 0., 0.], "Uczniowie, wychow., słuchacze": [0., 0., 0.],
                                         "Regon jednostki sprawozdawczej": [1, 2, 1], "Regon": [1, 2, 3]}),
                           (0, 4), (3, 4)),
                          (pd.DataFrame({"Nauczyciele": [0., 10., 10.], "Uczniowie, wychow., słuchacze": [10., 1., 6.],
                                         "Regon jednostki sprawozdawczej": [1, 2, 3], "Regon": [1, 2, 3]}), (2, 4),
                           (1, 4)),
                          (pd.DataFrame({"Nauczyciele": [0., 15., 0.], "Uczniowie, wychow., słuchacze": [10., 0., 3.],
                                         "Regon jednostki sprawozdawczej": [2, 2, 2], "Regon": [1, 2, 3]}),
                           (3, 4), (0, 4))])
def test_correct_schools_with_missing_teachers(df, expected1, expected2):
    result1, result2 = correct_schools_with_missing_teachers(df)
    assert result1.shape == expected1
    assert result2.shape == expected2


@pytest.fixture(scope='session')
def excel_file_multiple_sheets(tmpdir_factory):
    df1 = pd.DataFrame({'col1': [1, 2, 3, 4, 5, 6, 7],
                        'col2': [11, 12, 13, 14, 15, 16, 17]})
    df2 = pd.DataFrame({'col1': [i for i in range(100)], 'col2': [i for i in range(100)]})
    filename = str(tmpdir_factory.mktemp('data').join('data2.xlsx'))
    with pd.ExcelWriter(filename) as writer:
        df1.to_excel(writer, sheet_name='Woj 1', index=False)
        df2.to_excel(writer, sheet_name='Woj 2', index=False)
        writer.save()
    return filename


def test_load_inhabitants_file(excel_file_multiple_sheets):
    df_dict = load_inhabitants_file(excel_file_multiple_sheets)
    assert 'Woj 1' in df_dict
    assert 'Woj 2' in df_dict
    assert df_dict['Woj 1'].shape == (1, 2)
    assert df_dict['Woj 2'].shape == (94, 2)


def test_load_inhabitants_file_wrong_file():
    with pytest.raises(FileExistsError):
        load_inhabitants_file("../../data")


def test_load_inhabitants_file_wrong_type():
    with pytest.raises(Exception):
        load_inhabitants_file("../../data/profiler_results/data_process.png")


def test_rename_columns_inhabitants():
    df_dict = {'first_df': pd.DataFrame({('Wyszczególnienie\nSpecification', 'Unnamed: 0_level_1'): [0],
                                         ('Identyfikator terytorialny\nCode', 'Unnamed: 1_level_1'): [0],
                                         ('Ogółem \nTotal', 'Unnamed: 2_level_1'): [0],
                                         ('Mężczyźni Males', 'Unnamed: 3_level_1'): [0],
                                         ('Kobiety \nFemales', 'Unnamed: 4_level_1'): [0],
                                         ('Miasta  Urban areas', 'razem \ntotal'): [0],
                                         ('Miasta  Urban areas', 'mężczyźni males'): [0],
                                         ('Miasta  Urban areas', 'kobiety \nfemales'): [0],
                                         ('Wieś   Rural areas', 'razem \ntotal'): [0],
                                         ('Wieś   Rural areas', 'mężczyźni males'): [0],
                                         ('Wieś   Rural areas', 'kobiety \nfemales'): [0]})}
    result = rename_columns_inhabitants(df_dict)
    assert list(result['first_df'].columns) == ['Wyszczególnienie', 'Identyfikator terytorialny', 'Ogółem',
                                                'Mężczyźni Males', 'Kobiety', 'Miasta razem', 'Miasta',
                                                'Miasta kobiety', 'Wieś razem', 'Wieś', 'Wieś kobiety']


def test_fill_missing_id_values_inhabitants():
    df_dict = {
        'df': pd.DataFrame({"Identyfikator terytorialny": [2464011.0, '       ', '       ', '0464011', '       ']})}
    result = fill_missing_id_values_inhabitants(df_dict)
    assert 'Id' in result['df']
    assert 'Id rodzaj' in result['df']
    assert 'Identyfikator terytorialny' not in result['df']
    assert result['df']['Id'].values.tolist() == ['246401', '246401', '246401', '046401', '046401']

