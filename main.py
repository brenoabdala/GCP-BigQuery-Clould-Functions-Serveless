import functions_framework
import pandas as pd
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
import os

def main():
    path_json = "#.json"

    if os.path.exists(path_json):
        client = bigquery.Client.from_service_account_json(path_json)
    else:
        client = bigquery.Client()


    project_id = client.project 
    dataset_name = "dataset_GCP_Functions"
    table_name = "tabela_vendas_2"
    dataset_id = f"{project_id}.{dataset_name}"
    table_id = f"{dataset_id}.{table_name}"

    try:
        client.get_dataset(dataset_id)
        status_ds = f"Dataset '{dataset_name}' verificado."
    except NotFound:
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US" # "southamerica-east1" 
        client.create_dataset(dataset)
        status_ds = f"Dataset '{dataset_name}' criado agora."

    dados = pd.DataFrame([
        {"id": 1, "produto": "Notebook", "valor": 4500.00},
        {"id": 2, "produto": "Monitor", "valor": 1200.00},
        {"id": 3, "produto": "Teclado Mech", "valor": 350.00}
    ])

    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND") # WRITE_TRUNCATE, WRITE_EMPTY
    job = client.load_table_from_dataframe(dados, table_id, job_config=job_config)
    job.result() 

    sql_delete = f"DELETE FROM `{table_id}` WHERE id = 2"
    client.query(sql_delete).result()


    sql_select = f"SELECT * FROM `{table_id}`"
    df_final = client.query(sql_select).to_dataframe()
    
    return {
        "status_dataset": status_ds,
        "linhas_inseridas": len(dados),
        "preview": df_final.to_dict(orient='records')
    }

    # return df_final.to_dict(orient='records')
# main()
@functions_framework.http
def hello_get(request):
    """Entry point da Cloud Function"""
    try:
        processamento = main()
        return {
            "mensagem": "Executado com sucesso no GCP!",
            "detalhes": processamento
        }, 200
    except Exception as e:
        return {"erro": str(e)}, 500
