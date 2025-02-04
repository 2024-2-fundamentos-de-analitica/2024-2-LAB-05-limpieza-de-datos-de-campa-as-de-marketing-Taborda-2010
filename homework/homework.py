"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

    return

import pandas as pd
import zipfile
import os

def clean_campaign_data():
    input_directory = 'files/input/'
    output_directory = 'files/output/'

    # Create output folder if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Initialize empty DataFrames for each output file
    cliente_data = pd.DataFrame(columns=['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage'])
    campania_data = pd.DataFrame(columns=['client_id', 'number_contacts', 'contact_duration', 'previous_campaign_contacts', 'previous_outcome', 'campaign_outcome', 'last_contact_date'])
    economia_data = pd.DataFrame(columns=['client_id', 'cons_price_idx', 'euribor_three_months'])

    # Process each zip file in the input folder
    for archivo in os.listdir(input_directory):
        if archivo.endswith('.zip'):
            with zipfile.ZipFile(os.path.join(input_directory, archivo), 'r') as zip_file:
                for csv_archivo in zip_file.namelist():
                    with zip_file.open(csv_archivo) as file:
                        df = pd.read_csv(file)
                        #cliente
                        datos_cliente = df[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']].copy()
                        datos_cliente['job'] = datos_cliente['job'].str.replace('.', '').str.replace('-', '_')
                        datos_cliente['education'] = datos_cliente['education'].str.replace('.', '_').replace('unknown', pd.NA)
                        datos_cliente['credit_default'] = datos_cliente['credit_default'].apply(lambda x: 1 if x == 'yes' else 0)
                        datos_cliente['mortgage'] = datos_cliente['mortgage'].apply(lambda x: 1 if x == 'yes' else 0)
                        cliente_data = pd.concat([cliente_data, datos_cliente], ignore_index=True)
                        #campaña
                        datos_campania = df[['client_id', 'number_contacts', 'contact_duration', 'previous_campaign_contacts', 'previous_outcome', 'campaign_outcome', 'day', 'month']].copy()
                        datos_campania['previous_outcome'] = datos_campania['previous_outcome'].apply(lambda x: 1 if x == 'success' else 0)
                        datos_campania['campaign_outcome'] = datos_campania['campaign_outcome'].apply(lambda x: 1 if x == 'yes' else 0)
                        meses = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
                        datos_campania['month'] = datos_campania['month'].map(meses)
                        datos_campania['last_contact_date'] = pd.to_datetime(datos_campania[['day', 'month']].assign(year=2022).rename(columns={'day': 'day', 'month': 'month'}))
                        datos_campania.drop(columns=['month', 'day'], inplace=True)
                        campania_data = pd.concat([campania_data, datos_campania], ignore_index=True)
                        #economia
                        datos_economia = df[['client_id', 'cons_price_idx', 'euribor_three_months']].copy()
                        economia_data = pd.concat([economia_data, datos_economia], ignore_index=True)
    # Save the cleaned data to CSV files
    cliente_data.to_csv(os.path.join(output_directory, 'client.csv'), index=False)
    campania_data.to_csv(os.path.join(output_directory, 'campaign.csv'), index=False)
    economia_data.to_csv(os.path.join(output_directory, 'economics.csv'), index=False)

if __name__ == "__main__":
    clean_campaign_data()
