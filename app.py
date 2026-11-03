from pathlib import Path
import sys, joblib, pandas as pd, streamlit as st
ROOT=Path(__file__).resolve().parent; sys.path.insert(0,str(ROOT/'scripts'))
from pipeline import NUMS,CATS
st.set_page_config(page_title='Real Estate Investment Advisor',page_icon='🏠',layout='wide')
st.title('🏠 Real Estate Investment Advisor')
st.caption('Decision support from the provided India housing dataset. Forecasts use the project’s assumed city growth rates; they are not market guarantees.')
@st.cache_resource
def models(): return joblib.load(ROOT/'models/investment_classifier.joblib'),joblib.load(ROOT/'models/five_year_price_regressor.joblib')
try: clf,reg=models()
except Exception: st.error('Models not found. Run `python scripts/run_all.py` first.'); st.stop()
@st.cache_data
def listings():
 return pd.read_csv(ROOT/'data/processed/india_housing_processed.csv',usecols=CATS)
df=listings()
st.sidebar.header('Property details')
row={}
row['State']=st.sidebar.selectbox('State',sorted(df['State'].dropna().unique()))
state_rows=df.loc[df['State'].eq(row['State'])]
row['City']=st.sidebar.selectbox('City',sorted(state_rows['City'].dropna().unique()))
city_rows=state_rows.loc[state_rows['City'].eq(row['City'])]
row['Locality']=st.sidebar.selectbox('Locality',sorted(city_rows['Locality'].dropna().unique()))
for c in CATS[3:]:
 vals=sorted(df[c].dropna().astype(str).unique()); row[c]=st.sidebar.selectbox(c,vals)
row['BHK']=st.sidebar.number_input('Bedrooms (BHK)',1,10,3)
row['Size_in_SqFt']=st.sidebar.number_input('Area (sq ft)',200,20000,1200)
row['Price_in_Lakhs']=st.sidebar.number_input('Current price (lakhs)',1.0,100000.0,100.0)
row['Year_Built']=st.sidebar.number_input('Year built',1950,2026,2015)
row['Age_of_Property']=2026-row['Year_Built']; row['Price_per_SqFt']=row['Price_in_Lakhs']*100000/row['Size_in_SqFt']
row['Total_Floors']=st.sidebar.number_input('Total floors',1,100,10)
row['Floor_No']=st.sidebar.number_input('Floor number',0,int(row['Total_Floors']),min(2,int(row['Total_Floors'])))
row['Nearby_Schools']=st.sidebar.number_input('Nearby schools',0,50,3); row['Nearby_Hospitals']=st.sidebar.number_input('Nearby hospitals',0,50,2)
row['School_Density_Score']=row['Nearby_Schools']/row['Size_in_SqFt']*1000; row['Hospital_Density_Score']=row['Nearby_Hospitals']/row['Size_in_SqFt']*1000
if st.button('Analyze property',type='primary'):
 x=pd.DataFrame([{c:row[c] for c in NUMS+CATS}]); label=int(clf.predict(x)[0]); conf=float(clf.predict_proba(x)[0,label]); future=float(reg.predict(x)[0])
 a,b=st.columns(2); a.metric('Investment screen','Good investment' if label else 'Review carefully',f'{conf:.0%} model confidence'); b.metric('Estimated price after five years',f'₹{future:,.2f} lakhs',f"Assumed model growth from ₹{row['Price_in_Lakhs']:,.2f} lakhs")
 st.info('The classification compares estimated price per sq ft with the historical city median. The five year target is a synthetic city growth scenario (5%–9% yearly) because the dataset contains no future sale records.')
 st.subheader('Most influential features'); imp=clf.named_steps['model'].feature_importances_; names=clf.named_steps['prep'].get_feature_names_out(); st.bar_chart(pd.Series(imp,index=names).nlargest(12))
st.divider(); st.subheader('Dataset insights')
cols=st.columns(2)
for c,f in zip(cols,['city_price_per_sqft.png','price_distribution.png']):
 p=ROOT/'reports/figures'/f
 if p.exists(): c.image(str(p),width='stretch')
