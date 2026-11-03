from pathlib import Path
import json, warnings
import numpy as np, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier, ExtraTreesRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score, confusion_matrix, mean_absolute_error, mean_squared_error, r2_score
import joblib
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; OUT=DATA/'processed'; MODELS=ROOT/'models'; REPORT=ROOT/'reports'; FIG=REPORT/'figures'
TARGETS=['Good_Investment','Future_Price_5Y_Lakhs']
CATS=['State','City','Locality','Property_Type','Furnished_Status','Public_Transport_Accessibility','Parking_Space','Security','Amenities','Facing','Owner_Type','Availability_Status']
NUMS=['BHK','Size_in_SqFt','Price_in_Lakhs','Price_per_SqFt','Year_Built','Age_of_Property','Floor_No','Total_Floors','Nearby_Schools','Nearby_Hospitals','School_Density_Score','Hospital_Density_Score']

def load_and_prepare():
 df=pd.read_csv(DATA/'india_housing_prices.csv').drop_duplicates().copy()
 # Recompute derived fields from source to avoid trusting inconsistent supplied calculations.
 df['Price_per_SqFt']=df['Price_in_Lakhs']*100000/df['Size_in_SqFt'].clip(lower=1)
 df['Age_of_Property']=(2026-pd.to_numeric(df['Year_Built'],errors='coerce')).clip(lower=0)
 df['School_Density_Score']=df['Nearby_Schools']/df['Size_in_SqFt'].clip(lower=1)*1000
 df['Hospital_Density_Score']=df['Nearby_Hospitals']/df['Size_in_SqFt'].clip(lower=1)*1000
 med=df.groupby('City')['Price_per_SqFt'].transform('median')
 df['Good_Investment']=(df['Price_per_SqFt']<=med).astype(int)
 # Educational proxy target: deterministic city-specific annual growth assumption (5%-9%), compounded for five years.
 cities=sorted(df['City'].dropna().unique()); rates={c:0.05+0.04*i/max(1,len(cities)-1) for i,c in enumerate(cities)}
 df['Assumed_Annual_Growth_Rate']=df['City'].map(rates)
 df['Future_Price_5Y_Lakhs']=df['Price_in_Lakhs']*(1+df['Assumed_Annual_Growth_Rate'])**5
 OUT.mkdir(parents=True,exist_ok=True); df.to_csv(OUT/'india_housing_processed.csv',index=False)
 (REPORT/'target_assumptions.json').write_text(json.dumps({'good_investment':'1 when recomputed price per sq ft is at or below the median for its city; 0 otherwise.','future_price':'Current price compounded for five years using deterministic city growth rates evenly spanning 5%-9% annual. Synthetic proxy; not observed future outcomes.','year_reference':2026,'city_growth_rates':rates},indent=2))
 return df

def make_pipeline(model, scale=False):
 numeric=Pipeline([('imputer',SimpleImputer(strategy='median'))]+([('scale',StandardScaler())] if scale else []))
 cat=Pipeline([('imputer',SimpleImputer(strategy='most_frequent')),('onehot',OneHotEncoder(handle_unknown='ignore',min_frequency=10))])
 prep=ColumnTransformer([('num',numeric,NUMS),('cat',cat,CATS)])
 return Pipeline([('prep',prep),('model',model)])

def train(df):
 MODELS.mkdir(exist_ok=True)
 # deterministic row split; training full 250k with tree caps for a practical local run
 # Stratified 50k training/evaluation sample keeps the end-to-end run practical on a laptop.
 sample=df.sample(n=min(50000,len(df)),random_state=42)
 features=sample[NUMS+CATS]
 Xtr,Xte,ytr,yte=train_test_split(features,sample['Good_Investment'],test_size=.2,random_state=42,stratify=sample['Good_Investment'])
 clf=make_pipeline(RandomForestClassifier(n_estimators=60,max_depth=18,min_samples_leaf=3,n_jobs=-1,class_weight='balanced',random_state=42))
 clf.fit(Xtr,ytr); cp=clf.predict(Xte); prob=clf.predict_proba(Xte)[:,1]
 cm=confusion_matrix(yte,cp).tolist()
 cls={'accuracy':accuracy_score(yte,cp),'precision':precision_score(yte,cp,zero_division=0),'recall':recall_score(yte,cp,zero_division=0),'f1':f1_score(yte,cp,zero_division=0),'roc_auc':roc_auc_score(yte,prob),'confusion_matrix':cm}
 Xtr,Xte,ytr,yte=train_test_split(features,sample['Future_Price_5Y_Lakhs'],test_size=.2,random_state=42)
 reg=make_pipeline(ExtraTreesRegressor(n_estimators=60,max_depth=22,min_samples_leaf=2,n_jobs=-1,max_features=.8,random_state=42))
 reg.fit(Xtr,ytr); rp=reg.predict(Xte)
 regm={'rmse':mean_squared_error(yte,rp)**.5,'mae':mean_absolute_error(yte,rp),'r2':r2_score(yte,rp)}
 joblib.dump(clf,MODELS/'investment_classifier.joblib'); joblib.dump(reg,MODELS/'five_year_price_regressor.joblib')
 metrics={'classification':cls,'regression':regm,'n_rows':len(df),'n_features':len(NUMS+CATS),'test_size':len(yte)}
 (REPORT/'metrics.json').write_text(json.dumps(metrics,indent=2))
 # MLflow experiment tracking; log artifacts and register models when available.
 try:
  import mlflow, mlflow.sklearn
  mlflow.set_tracking_uri(f"sqlite:///{ROOT/'mlflow.db'}"); mlflow.set_experiment('Real Estate Investment Advisor')
  for name,model,ms in [('investment_classifier',clf,cls),('five_year_price_regressor',reg,regm)]:
   with mlflow.start_run(run_name=name):
    mlflow.log_params({'model':type(model.named_steps['model']).__name__,'random_state':42,'test_fraction':.2,'rows':len(df),'model_sample_rows':len(sample)})
    mlflow.log_metrics({k:v for k,v in ms.items() if isinstance(v,(int,float))})
    mlflow.sklearn.log_model(model,name='model',registered_model_name=name,serialization_format='cloudpickle')
    mlflow.log_artifact(str(REPORT/'target_assumptions.json'))
 except Exception as e: (REPORT/'mlflow_status.txt').write_text(f'MLflow logging could not complete: {e}\nInstall requirements and rerun scripts/run_all.py.')
 return metrics

def main():
 warnings.filterwarnings('ignore'); df=load_and_prepare(); train(df)
 print('Prepared',len(df),'rows; metrics:',(REPORT/'metrics.json').read_text())
if __name__=='__main__': main()
