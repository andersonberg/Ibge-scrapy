import pandas as pd
import cobertura.cobertura_nordeste as cobertura


def test_get_equipments():
    equipamentos = pd.read_excel("Planilhas/Equipamentos por município.xls")
    equipamentos_por_cidade = equipamentos[equipamentos["cidade"] == 210120]
    total_sum = cobertura.get_equipments(equipamentos_por_cidade)
    assert len(total_sum.keys()) == 5
    assert "XP" in total_sum.keys()
    assert "US" in total_sum.keys()
    assert "MR" in total_sum.keys()
    assert "CT" in total_sum.keys()
    assert "MI" in total_sum.keys()


def test_get_city_assist():
    ans = pd.read_excel("Planilhas/ANS Vidas Assistidas NE.xls")
    city_assist = cobertura.get_city_assist(ans, 210120)
    assert type(city_assist) == int


def test_get_city_assist_zero():
    ans = pd.read_excel("Planilhas/ANS Vidas Assistidas NE.xls")
    city_assist = cobertura.get_city_assist(ans, 2503753)
    assert city_assist == 0


def test_get_city_pib():
    pib = pd.read_excel("Planilhas/PIBMunicipal2008-2012.xls", header=5, parse_cols="A,F,G")
    pib = pib[1666:1768]
    city_name = 'Viçosa'
    city_pib, city_pib_per_capita = cobertura.get_city_pib(pib, city_name)
    assert type(city_pib) == float
    assert type(city_pib_per_capita) == float


def test_get_pib_by_state():
    pib_state = cobertura.get_pib_by_state('pernambuco')
    assert pib_state.shape[0] > 0
    assert pib_state.shape[1] > 0


def test_state_coverage():
    equipamentos = pd.read_excel("Planilhas/Equipamentos por município.xls")
    ans = pd.read_excel("Planilhas/ANS Vidas Assistidas NE.xls")
    state_name = 'pernambuco'
    city_list = cobertura.state_coverage(state_name, equipamentos, ans)
    assert len(city_list) > 0


def test_create_states_coverage():
    states_dataframe = cobertura.create_states_coverage()
    assert states_dataframe.shape[0] > 0
    assert states_dataframe.shape[1] > 0
