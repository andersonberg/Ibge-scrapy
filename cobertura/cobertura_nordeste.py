# coding: utf-8
import pandas as pd
import numpy as np

estados = {
     'maranhao': (460, 677),
     'piaui': (678, 902),
     'ceara': (903, 1087),
     'rio grande do norte': (1088, 1255),
     'paraiba': (1256, 1479),
     'pernambuco': (1480, 1665),
     'alagoas': (1666, 1768),
     'sergipe': (1769, 1844),
     'bahia': (1845, 2262)
}


def get_equipments(equip):
    # raio_x = equip[equip["equipamento"].map(lambda x: "raio x" in x.encode('utf8').lower() and "dentario" not in x.encode('utf8').lower() and "densitometria" not in x.encode('utf8').lower())]
    raio_x = equip[equip["equipamento"].map(lambda x: "raio x" in x.lower() and "dentario" not in x.lower() and "densitometria" not in x.lower())]
    mamografo = equip[equip["equipamento"].map(lambda x: "mamografo" in x.lower())]
    ultrassom = equip[equip["equipamento"].map(lambda x: "ultrassom" in x.lower())]
    ressonancia = equip[equip["equipamento"].map(lambda x: "ressonancia" in x.lower())]
    tomografo = equip[equip["equipamento"].map(lambda x: "tomógrafo" in x.lower())]
    pet_ct = equip[equip["equipamento"].map(lambda x: "pet/ct" in x.lower())]
    gama = equip[equip["equipamento"].map(lambda x: "gama" in x.lower())]

    equipments_totals = {"XP": 0, "US": 0, "MR": 0, "CT": 0, "MI": 0}

    sum_raio_x = 0
    sum_ultrassom = 0
    sum_ressonancia = 0
    sum_tomografo = 0
    sum_pet = 0
    if not raio_x.empty:
        sum_raio_x = raio_x["existentes"].sum()
    if not mamografo.empty:
        sum_raio_x += mamografo["existentes"].sum()
    if not ultrassom.empty:
        sum_ultrassom = ultrassom["existentes"].sum()
    if not ressonancia.empty:
        sum_ressonancia = ressonancia["existentes"].sum()
    if not tomografo.empty:
        sum_tomografo = tomografo["existentes"].sum()
    if not pet_ct.empty:
        sum_pet = pet_ct["existentes"].sum()
    if not gama.empty:
        sum_pet += gama["existentes"].sum()

    equipments_totals.update({"XP": sum_raio_x})
    equipments_totals.update({"US": sum_ultrassom})
    equipments_totals.update({"MR": sum_ressonancia})
    equipments_totals.update({"CT": sum_tomografo})
    equipments_totals.update({"MI": sum_pet})

    return equipments_totals


def get_city_assist(ans, city_code):
    # Obtém a quantidade de vidas assistidas por cidade
    city_lifes_data = ans[ans[u"Município"].map(lambda x: str(city_code) in x)]

    if city_lifes_data.empty:
        city_assist = 0
    else:
        city_assist = int(city_lifes_data[u"Assistência_Médica"])

    return city_assist


def get_city_pib(pib, city_name):
    # Obtém PIB e PIB per capita
    city_pib_dataframe = pib[pib[u"Município"] == city_name]

    if city_pib_dataframe.empty:
        city_pib = 0
        city_pib_per_capita = 0
    else:
        city_pib = float(city_pib_dataframe[2012])
        city_pib_per_capita = float(city_pib_dataframe[u"Per capita (R$) 2012"])

    return city_pib, city_pib_per_capita


def get_pib_by_state(state):
    state_range = estados.get(state)
    if len(state_range) > 1:
        start_row = state_range[0]
        end_row = state_range[1]

        pib = pd.read_excel("Planilhas/PIBMunicipal2008-2012.xls", header=5, parse_cols="A,F,G")
        pib = pib[start_row:end_row]

        return pib


def state_coverage(state_name, equipamentos, ans):
    pib = get_pib_by_state(state_name)
    state_name_formated = state_name.replace(' ', '_')
    total_population_sheet = 'Planilhas/Nordeste/total_populacao_' + state_name_formated.lower() + '.xls'
    populacao = pd.read_excel(total_population_sheet)
    city_list = []
    for row in populacao.iterrows():
        try:
            city_code = int(row[1][u"Código do município"][:-1])
            city_pop = int(row[1][u"Total da população 2010"])
            city_name = row[1][u"Nome do município"]

            # Obtém a quantidade de vidas assistidas por cidade
            city_assist = get_city_assist(ans, city_code)

            # Obtém PIB e PIB per capita
            city_pib, city_pib_per_capita = get_city_pib(pib, city_name)

            info_dict = {u"Município": city_name,
                         u"Produto Interno Bruto (R$ 1.000 )": city_pib,
                         u"PIB per capita (R$)": city_pib_per_capita,
                         u"Quantidade (Pessoas)": city_pop,
                         "Vidas Assistidas ANS": city_assist}

            # Obtém a quantidade de máquinas por categoria
            equipamentos_por_cidade = equipamentos[equipamentos["cidade"] == city_code]
            total_sum = get_equipments(equipamentos_por_cidade)

            info_dict.update(total_sum)
            city_list.append(info_dict)

        except ValueError:
            print('ValueError')
            print(row)
            continue
        except TypeError:
            print('TypeError')
            print(row)
            continue

    return city_list


def create_states_coverage():
    equipamentos = pd.read_excel("Planilhas/Equipamentos por município.xls")
    ans = pd.read_excel("Planilhas/ANS Vidas Assistidas NE.xls")
    for state_name in estados.keys():
        city_list = state_coverage(state_name, equipamentos, ans)
        columns = [u"Município",
                   u"Produto Interno Bruto (R$ 1.000 )",
                   u"PIB per capita (R$)",
                   u"Quantidade (Pessoas)",
                   "Vidas Assistidas ANS",
                   "XP", "US", "MR", "CT", "MI"]
        state_dataframe = pd.DataFrame(columns=columns)
        state_dataframe = state_dataframe.append(city_list, ignore_index=True)
        xls_filename = 'Cobertura ' + state_name.upper() + '.xls'
        writer = pd.ExcelWriter(xls_filename)
        state_dataframe.to_excel(writer, index=False)
        writer.save()


if __name__ == '__main__':
    create_states_coverage()
