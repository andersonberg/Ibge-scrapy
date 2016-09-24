import pandas as pd
from cobertura.cobertura_nordeste import get_equipments, get_city_assist, get_city_pib


def test_get_equipments():
    equipamentos = pd.read_excel("Planilhas/Equipamentos por município.xls")
    equipamentos_por_cidade = equipamentos[equipamentos["cidade"] == 210120]
    total_sum = get_equipments(equipamentos_por_cidade)
    assert len(total_sum.keys()) == 5
    assert "XP" in total_sum.keys()
    assert "US" in total_sum.keys()
    assert "MR" in total_sum.keys()
    assert "CT" in total_sum.keys()
    assert "MI" in total_sum.keys()


def test_get_city_assist():
    ans = pd.read_excel("Planilhas/ANS Vidas Assistidas NE.xls")
    city_assist = get_city_assist(ans, 210120)
    assert type(city_assist) == int


def test_get_city_pib():
    pib = pd.read_excel("Planilhas/PIBMunicipal2008-2012.xls", header=5, parse_cols="A,F,G")
    pib = pib[1666:1768]
    city_name = 'Viçosa'
    city_pib, city_pib_per_capita = get_city_pib(pib, city_name)
    assert type(city_pib) == float
    assert type(city_pib_per_capita) == float
