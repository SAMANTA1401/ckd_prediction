import os
import sys
from src.exception import CustomException
from src.logger import logging

import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformationConfig
from src.components.data_transformation import DataTransformation

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

# 7. after EDA
@dataclass
class DataIngestionConfig:  
    raw_data_path: str=os.path.join('artifacts','data.csv') #save raw dataset in this path
    train_data_path: str=os.path.join('artifacts','train.csv') #save train data in this path
    test_data_path:str = os.path.join('artifacts', 'test.csv')   # save test data in this path

# 8.
class DataIngestion:
    # 8.1
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    # 8.2
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            df = pd.read_csv('notebook\data\kidney_disease.csv')

            ## drop id
            df.drop(columns=['id'],axis=1,inplace=True)    
            ### handle noice values
            df['pcv']=df['pcv'].apply(lambda x: '41' if x=='\t?' or x=='\t43'  else x)
            df['wc']=df['wc'].apply(lambda x: '9800' if x=='\t6200'or x=='\t8400' or x=='\t?'  else x)
            df['rc']=df['rc'].apply(lambda x: '5.2' if x=='\t?'  else x)
            df['dm']=df['dm'].apply(lambda x: 'no' if x=='\tno' else x)
            df['dm']=df['dm'].apply(lambda x: 'yes' if x==' yes'or x=='\tyes'  else x)
            df['cad']=df['cad'].apply(lambda x: 'no' if x=='\tno' else x)
            df['classification']=df['classification'].apply(lambda x: 'ckd' if x=='ckd\t'  else x)

            ### converting pcv, wc rc columns  to numeric values
            df = df.astype({'pcv':'float','wc':'float', 'rc': 'float'})
            # df = df.astype({'age':'float32', 'bp':'float32', 'sg':'float32', 'al':'float32', 'su':'float32', 'bgr':'float32', 'bu':'float32', 'sc':'float32', 'sod':'float32', 'pot':'float32', 'hemo':'float32','pcv':'float32','wc':'float32','rc':'float32'})
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True) # create "artifacts" directory if not exist if exist delete and recreate
            
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)

            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info('Ingestion of the data is completed')

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise logging.info(CustomException(e,sys))
            
# before data transformation            
# 9. run:python -m src.components.data_ingestion
if __name__=="__main__":
    obj = DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()

# run:python -m src.components.data_ingestion        then go model trainner  component
## 13 .
    data_transformation = DataTransformation()
##18 then go to application.py
    train_arr, test_arr,_ = data_transformation.initiate_data_transformation(train_data,test_data)

    modeltrainer = ModelTrainer()
    model_name,f1_sco,accuracy=modeltrainer.initiate_model_trainer(train_arr,test_arr)
    print(f"Model Name:{model_name} , f1_Score :{f1_sco} , Accuracy: {accuracy}")