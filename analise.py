import pandas as pd
import matplotlib.pyplot as plt
from numpy import arange
import os

def ensure_directory_exists(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)

def is_dataframe(obj) -> bool:
    return isinstance(obj, pd.DataFrame)

def column_in_dataframe(column: str, df: pd.DataFrame) -> bool:
    if not is_dataframe(df):
        raise ValueError("The provided object is not a DataFrame.")
    return column in df.columns

def generate_bar_graphic(df: pd.DataFrame, column: str,
                  bars_quantity: int, title: str, image_name: str,
                  output_directory: str = 'imagens_analise') -> None:
    
    if not is_dataframe(df):
        raise ValueError("The provided object is not a DataFrame.")
    
    if not column_in_dataframe(column, df):
        raise ValueError(
            f"The column '{column}' does not exist in the DataFrame.")
    
    if type(bars_quantity) is not int or bars_quantity <= 0:
        raise ValueError("The 'bars_quantity' must be a positive integer.")
    
    ensure_directory_exists(output_directory)
    
    plt.figure(figsize=(15, 5))
    if bars_quantity >= 10:
        df.value_counts(column)[:bars_quantity].sort_values().plot(
            kind='barh', color=plt.cm.Set1(arange(bars_quantity-1, -1, -1)))
        plt.xticks(fontsize=20, rotation=0)
    else:
        df.value_counts(column)[:bars_quantity].plot(
            kind='bar', color=plt.cm.Set2(arange(bars_quantity)))
        plt.xticks(rotation=0, fontsize=20)
    plt.title(title, fontdict={'fontsize': 20, 'fontweight':'bold'})
    plt.xlabel(column, fontdict={'fontsize': 20})
    plt.ylabel('Contagem', fontdict={'fontsize': 20})
    plt.yticks(fontsize=20)
    name_image_file: str = f'{output_directory}/{image_name}.png'
    plt.savefig(name_image_file, dpi=300, bbox_inches="tight")
    print(f'Graphic saved in: {name_image_file}')
    plt.show();
    return None

def generate_sector_graphic(
        df: pd.DataFrame, column: str, title: str, image_name: str) -> None:

    if not is_dataframe(df):
        raise ValueError("The provided object is not a DataFrame.")
    
    if not column_in_dataframe(column, df):
        raise ValueError(
            f"The column '{column}' does not exist in the DataFrame.")
    
    ensure_directory_exists('imagens_analise')

    sector_data: pd.DataFrame = df.value_counts(column).reset_index()
    sector_data.columns = [column, 'count']
    plt.figure(figsize=(10, 5))
    plt.title(title, fontdict={'fontsize': 20, 'fontweight':'bold'})
    plt.pie(
        sector_data['count'], labels=sector_data[column],
        colors=['red', 'blue'] if column == 'Necessita de PAEBM' else ['blue', 'red'],
        autopct="%0.2f%%", textprops={'fontsize': 20})
    name_image_file: str = f'imagens_analise/{image_name}.png'
    plt.savefig(name_image_file, dpi=300, bbox_inches="tight")
    print(f'Graphic saved in: {name_image_file}')
    plt.show();
    return None


if __name__ == '__main__':
    data_dam_mining: pd.DataFrame = pd.read_csv(
        'data/barragens.csv', sep=';', encoding='latin-1')

    #data_dam_mining['column_name'].isnull().sum()
    #data_dam_mining.value_counts('column_name')

    generate_bar_graphic(
        data_dam_mining, 'Empreendedor',
        10, '10 empresas com maior quantidade de barragens contruídas.',
        'empreendedor')

    generate_bar_graphic(
        data_dam_mining,'UF',
        10, '10 estados com maior quantidade de barragens contruídas.',
        'uf')

    generate_bar_graphic(
        data_dam_mining,'Categoria de Risco - CRI',
        4, 'Quantidade de barragens em relação a CRI',
        'cri')

    generate_bar_graphic(
        data_dam_mining,'Dano Potencial Associado - DPA',
        4, 'Quantidade de barragens em relação ao DPA',
        'dpa')

    generate_sector_graphic(data_dam_mining, 'Necessita de PAEBM',
                'As barragens estão inclusas no PAEBM?', 'paebm')

    generate_sector_graphic(data_dam_mining, 'Inserido na PNSB',
                            'As barragens estão inclusas na PNSB?', 'pnsb')

    generate_bar_graphic(
        data_dam_mining,'Nível de Emergência',
        4, 'Quantidade de barragens em relação ao nível de emergência',
        'nivel_emergencia')

    generate_bar_graphic(
        data_dam_mining, 'Minério principal presente no reservatório',
        10, '10 Principais minérios presentes nas barragens de mineração',
        'minerio_barragem')
