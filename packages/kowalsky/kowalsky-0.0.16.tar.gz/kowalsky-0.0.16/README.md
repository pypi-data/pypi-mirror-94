# Kowalsky, analysis!

A simple package for handful ML things and more.

What's inside?

1. ```analysis``` - method for evaluation of specified model with
   given dataframe. With ```export_test_set=True``` it exports
   ready for submission predictions.
   
2. df - module for working with dataframe:
    * ```corr``` - sort all correlated features.
    * ```handle_outliers``` - fill or drop columns with outliers.
    * ```log_transform``` - transform columns with log function.
    * ```group_by_mean``` - make additional columns with aggregated mean
    * ```group_by_max``` - make additional columns with aggregated max
    * ```group_by_min``` - make additional columns with aggregated min
    * ```scale``` - scale columns with Standard of MinMax scalers
    
3. kaggle:
    * ```submit``` - make submit-file for kaggle based on sample
    
4. metrics:
    *  ```rmse``` - RMSE scorer
    *  ```rmsle``` - RMSLE scorer
    
5. optuna - handful methods for working with optuna:
    * ```optimize``` - optimize model with given dataframe
    * ```optimize_super_learner``` - optimize super learner configuration
   with given set of models and set of heads (meta_model)
      
6. colab:
    *  ```csv``` - read csv file located at Google Drive with
       specified id
    *  ```path``` - get path to Google Drive file
   
## Example:
```
!pip install kowalsky --upgrade
from kowalsky.optuna import optimize
optimize('RFR',
         path='../input/project/feed.csv',
         scorer='acc',
         y_label='y_label',
         trials=3000)
```

## Avaliable models:
#### Gradient Boosts
```
    'XGBR': XGBRegressor
    'XGBC': XGBClassifier
    'LGBR': LGBMRegressor
    'LGBC': LGBMClassifier
```

#### Trees
```
    'RFR': RandomForestRegressor
    'RFC': RandomForestClassifier
    'DTR': DecisionTreeRegressor
    'DTC': DecisionTreeClassifier
    'ETR': ExtraTreeRegressor
    'ETC': ExtraTreeClassifier
```

#### Ensemble
```
    'BC': BaggingClassifier
    'BR': BaggingRegressor
    'ADAR': AdaBoostRegressor
    'ADAC': AdaBoostClassifier
    'CBR': CatBoostRegressor
    'CBC': CatBoostClassifier
```

#### KNeighbors
```
    'KNC': KNeighborsClassifier
    'KNR': KNeighborsRegressor
```

#### SVM
```
    'SVR': SVR
    'SVC': SVC
```
