## Summary of the article

The authors propose a 4 step method for performing interpretable cluster analysis. First the data must be preprocessed by removing any variables with too many missing values, any remaining missing values imputed, and outliers identified. Then dimensionality reduction should be performed on the dataset to reduce the number of variables. Here they use SPCA (Sparse Principal Component Analysis) for numeric variables and MCA (Multiple Correspondence Analysis) for categorical variables. This allows the results to be more easily interpreted and improves distance based clustering. Next clustering should be performed using k-means (default option). The number of clusters was determined using the elbow method. Finally, classification is performed to build a model that can predict the cluster labels. SHAP (SHapley Additive exPlanations) values are then used to determine which variables are important for each cluster.

## Why the results of clustering need to be interpreted

As clustering is an unsupervised learning technique, it will just return cluster numbers that have no meaning. Someone needs to interpret the data to find out why the clusters are different.

## Why classification helps

The cluster labels can be used as the target variable in a supervised model. The variables used to predict the cluster labels are what is separating the clusters. SHAP will also show if the variables are having a positive/negative effect. If the classifier uses the same variables as the clustering then it will give an interpretation of what the clusters represent but will not provide independent validation.

## Example

The second paper used this method to cluster students from the Programme for International Student Assessment (PISA) dataset (2022) of 30,800 students from Spain. This reduced the number of variables from 74 to 16 new variables. 7 clusters were formed. An XGBoost classifier was trained (accuracy = 0.8643). The main factors separating the student profiles were economic, social and cultural status and access to Information and Communications Technology (ICT) at home.

## Our Project

We will cluster the DC census tracts based on the time of occurrence of crime (proportion of crimes occurring at certain times of day, weekends and seasons). We will then classify the clusters based on the proportion of offenses and weapons. As the predictor variables are different to those used for clustering, this will interpret the clusters using independent information. The cluster labels will never be used as an input feature.
