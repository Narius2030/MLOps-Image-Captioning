import sys
sys.path.append('./airflow')

import os
import pickle
import pandas as pd
import concurrent.futures as cf
from datetime import datetime
from utils.config import get_settings
from utils.operators.text import TextOperator
from utils.operators.image import ImageOperator
from utils.operators.trinodb import SQLOperators
from utils.operators.storage import MinioStorageOperator
from utils.operators.mongodb import MongoDBOperator


settings = get_settings()
sql_opt = SQLOperators('imcp', settings)
mongo_operator = MongoDBOperator('imcp', settings.DATABASE_URL)
minio_operator = MinioStorageOperator(endpoint=f'{settings.MINIO_HOST}:{settings.MINIO_PORT}',
                                    access_key=settings.MINIO_USER,
                                    secret_key=settings.MINIO_PASSWD)




def load_image_storage(file_name:str, partition:str):
    try:
        minio_operator.upload_file('mlflow', f'/encoded-data/{partition}/{file_name}', f'{settings.EXTRACT_FEATURE_PATH}/{file_name}')
    except:
        raise Exception('Upload extracted feature file failed!')
    finally:
        os.remove(f'{settings.EXTRACT_FEATURE_PATH}/{file_name}')


def process_row(row):
    encoded_caption = TextOperator.encode_caption(row['tokenized_caption'])
    encoded_image = ImageOperator.encode_image(row['original_url'])
    return {
        "image_url": row['original_url'],
        "pixel_values": encoded_image['pixel_values'],
        "input_ids": encoded_caption['input_ids'],
        "attention_mask": encoded_caption['attention_mask']
    }

def load_encoded_data():
    file_names = []
    affected_rows = 0
    start_time = pd.to_datetime('now')
    latest_time = sql_opt.get_latest_fetching_time('gold', 'encoded_data')
    try:
        partition = datetime.now().strftime("%Y-%m-%d")
        metadata = {
            "root_url": f"{settings.MINIO_URL}/{partition}/encoded-data", 
            "date": datetime.today()
        }
        for batch in sql_opt.data_generator('refined', latest_time=latest_time, batch_size=10):
            encoded_data = []
            datarows = list(batch)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            # Sử dụng ProcessPoolExecutor cho CPU-bound tasks
            with cf.ProcessPoolExecutor(max_workers=2) as executor:
                encoded_data = list(executor.map(process_row, datarows))
            
            file_name = f"encoded_data_{timestamp}.pkl"
            with open(f"./airflow/data/{file_name}", "wb") as f:
                pickle.dump(encoded_data, f)
            load_image_storage(file_name, partition)
            
            print('SUCCESS with', len(datarows))
            affected_rows += len(datarows)
            file_names.append(file_name)
            break
        # write logs
        metadata["files"] = file_names
        metadata["encoding-type"] = "text"
        metadata["total_captions"] = affected_rows
        mongo_operator.insert_batches('featured', [metadata])
        sql_opt.write_log('extract_feature', layer='gold', start_time=start_time, status="SUCCESS", action="insert", affected_rows=affected_rows)
        
    except Exception as exc:
        sql_opt.write_log('extract_feature', layer='gold', start_time=start_time, status="ERROR", error_message=str(exc), action="insert", affected_rows=affected_rows)
        raise Exception(str(exc))



if __name__=='__main__':
    load_encoded_data() 