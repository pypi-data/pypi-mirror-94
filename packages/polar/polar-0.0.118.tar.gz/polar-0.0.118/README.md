polar
============

polar is a Python module that contains simple to use data science functions.
It is built on top of SciPy, scikit-learn, seaborn and pandas.

Installation
------------

If you already have a working installation of numpy and scipy,
the easiest way to install parkitny is using ``pip``:

    pip install polar seaborn pandas scikit-learn scipy matplotlib numpy nltk -U

Dependencies
------------

polar requires:
- Python (>= 3.5)
- NumPy (>= 1.11.0)
- SciPy (>= 0.17.0)
- Seaborn (>= 0.9.0)
- scikit-learn (>= 0.21.3)
- nltk (>= 3.4.5)
- python-pptx (>= 0.6.18)
- cryptography (> 2.8)
- imblearn

Jupyter Notebook Examples
------------

Here is the link to the jupyter notebook with all the exmples that are described below
[Polar-Examples](https://github.com/pparkitn/imagehost/blob/master/polar-examples.ipynb)


ACA (Automated Cohort Analysis) Example
------------

The ACA creates three heatmaps for each feature in the data set.
 - Conversion heatmap - conversion per feature value
 - Distribution heatmap - distribution per feature value
 - Size heatmap - total samples per feature value

Data File:
[ACA_date.csv](https://github.com/pparkitn/imagehost/blob/master/ACA_date.csv?raw=true)

Final Result Power Point:
[ACA.pptx](https://github.com/pparkitn/imagehost/blob/master/ACA.pptx?raw=true)

```python
import pandas as pd
import polar as pl
from pptx import Presentation
%matplotlib inline

url = "https://raw.githubusercontent.com/pparkitn/imagehost/master/ACA_date.csv"
data_df=pd.read_csv(url)

prs = Presentation()    
pl.create_title(prs,'ACA')
for chart in pl.ACA_create_graphs(data_df,'date','label'):
    pl.add_chart_slide(prs,chart[0],chart[1])
pl.save_presentation(prs,filename = 'ACA')
```

Conversion:
![Image](https://raw.githubusercontent.com/pparkitn/imagehost/master/var1conv_df.jpg)

Distribution:
![Image](https://raw.githubusercontent.com/pparkitn/imagehost/master/var1dist_df.jpg)

Samples:
![Image](https://raw.githubusercontent.com/pparkitn/imagehost/master/var1size_df.jpg)

EDA Example
------------

```python
import pandas as pd
import openml
import polar as pl

dataset = openml.datasets.get_dataset(31)
X, y, categorical_indicator, attribute_names = \
dataset.get_data(target=dataset.default_target_attribute,dataset_format='dataframe')

openml_df = pd.DataFrame(X)
openml_df['target'] = y

data_df = pl.analyze_correlation(openml_df,'target')
pl.get_heatmap(data_df,'correlation_heat_map.png',1.1,14,'0.1f',0,100,5,5)
```

![Image](https://github.com/pparkitn/imagehost/blob/master/heat_map_1.jpg?raw=true)

```python
data_df = pl.analyze_association(openml_df,'target',verbose=0)
pl.get_heatmap(data_df,'association_heat_map.png',1.1,12,'0.1f',0,100,10,10)

```

![Image](https://github.com/pparkitn/imagehost/blob/master/heat_map_2.jpg?raw=true)

```python
print(pl.analyze_df(openml_df, 'target',10))
```

![Image](https://github.com/pparkitn/imagehost/blob/master/analyze_df.jpg?raw=true)

```python
data_df = pl.get_important_features(openml_df,'target')
pl.get_bar(data_df,'bar.png','Importance','Feature_Name')
```

![Image](https://github.com/pparkitn/imagehost/blob/master/imp_features_bar.png?raw=true)


NLP Example
------------

```python
import nltk
nltk.download('wordnet')
import pandas as pd
import polar as pl
from cryptography.fernet import Fernet

url = "https://raw.githubusercontent.com/pparkitn/imagehost/master/test_real_or_not_from_kaggle.csv"
data_df=pd.read_csv(url)

data_df.drop(columns=['id','keyword','location'], inplace=True)
data_df.head(3)
```

![Image](https://github.com/pparkitn/imagehost/blob/master/nlp_start_df.PNG?raw=true)

```python
key = Fernet.generate_key()
data_df['text_encrypted'] =  data_df['text'].apply(pl.encrypt_df,args=(key,))
data_df['text_decrypted'] =  data_df['text_encrypted'].apply(pl.decrypt_df,args=(key,))

data_df['text_stem'] = data_df['text_decrypted'].apply(pl.nlp_text_process,args=('stem',))
data_df['text_stem_lem'] = data_df['text_stem'].apply(pl.nlp_text_process,args=('lem',))

data_df.head(3)
```
![Image](https://github.com/pparkitn/imagehost/blob/master/nlp_end_df.PNG?raw=true)


```python
cluster_df = pl.nlp_cluster(data_df, 'text_stem_lem',  10, 'text_cluster',1.0,1,100,1,'KMeans',(1,2))[0]
cluster_df.groupby(['text_cluster']).count()
```
![Image](https://github.com/pparkitn/imagehost/blob/master/nlp_text_clusters.PNG?raw=true)
```python
cluster_df[cluster_df['text_cluster']==9]['text_stem_lem']
```
![Image](https://github.com/pparkitn/imagehost/blob/master/nlp_cluster9.PNG?raw=true)
