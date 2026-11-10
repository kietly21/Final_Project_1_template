# Crime Analytics in Washington, D.C.

**Team members:** Myles Lewis, Kiet Ly

## Overview

This dataset contains a subset of crime locations within Washington, D.C., which are reported in the Analytical Services Application database by the District of Columbia Metropolitan Police Department.

The file used here is the 2025 incident file: 24,156 incident records covering 206 census tracts, with fields for offense type, method, start and report time, and several geographic units.

## Research Question

Are there "nightlife" type areas where crime concentrates late at night, and how do they differ from areas with daytime-dominant crime?

## Source

[Crime Incidents in 2025, DC Open Data](https://opendata.dc.gov/datasets/74d924ddc3374e3b977e6f002478cb9b_7/explore?location=38.888659%2C-76.991409%2C17)

---

# Session 1

## 1. Paper Summary

### Summary of the article

The authors propose a 4 step method for performing interpretable cluster analysis. First the data must be preprocessed by removing any variables with too many missing values, any remaining missing values imputed, and outliers identified. Then dimensionality reduction should be performed on the dataset to reduce the number of variables. Here they use SPCA (Sparse Principal Component Analysis) for numeric variables and MCA (Multiple Correspondence Analysis) for categorical variables. This allows the results to be more easily interpreted and improves distance based clustering. Next clustering should be performed using k-means (default option). The number of clusters was determined using the elbow method. Finally, classification is performed to build a model that can predict the cluster labels. SHAP (SHapley Additive exPlanations) values are then used to determine which variables are important for each cluster.

### Why the results of clustering need to be interpreted

As clustering is an unsupervised learning technique, it will just return cluster numbers that have no meaning. Someone needs to interpret the data to find out why the clusters are different.

### Why classification helps

The cluster labels can be used as the target variable in a supervised model. The variables used to predict the cluster labels are what is separating the clusters. SHAP will also show if the variables are having a positive/negative effect. If the classifier uses the same variables as the clustering then it will give an interpretation of what the clusters represent but will not provide independent validation.

### Example

The second paper used this method to cluster students from the Programme for International Student Assessment (PISA) dataset (2022) of 30,800 students from Spain. This reduced the number of variables from 74 to 16 new variables. 7 clusters were formed. An XGBoost classifier was trained (accuracy = 0.8643). The main factors separating the student profiles were economic, social and cultural status and access to Information and Communications Technology (ICT) at home.

### Our Project

We will cluster the DC census tracts based on the time of occurrence of crime (proportion of crimes occurring at certain times of day, weekends and seasons). We will then classify the clusters based on the proportion of offenses and weapons. As the predictor variables are different to those used for clustering, this will interpret the clusters using independent information. The cluster labels will never be used as an input feature.

## 2. Variable Selection

### Variable-Selection Table

| Variable | Description and unit | Data type | Proposed role | Rationale / preparation needed |
|---|---|---|---|---|
| START_DATE | Date and time the incident started (UTC, Coordinated Universal Time) | Datetime | Source for clustering inputs | Convert to Eastern time, then derive hour, weekday, and month. Keep only incidents that started in 2025 |
| REPORT_DAT | Date and time the incident was reported (UTC) | Datetime | Filter only | Used to drop incidents reported long after they started. Not a feature |
| Hour-of-day shares (per tract) | Proportion of a tract's incidents in each time block, such as 4-hour blocks | Numerical | Clustering input | Derived from START_DATE. Proportions rather than counts, so clusters reflect timing and not crime volume |
| Weekend share (per tract) | Proportion of a tract's incidents on Saturday or Sunday | Numerical | Clustering input | Derived from START_DATE |
| Seasonal share (per tract) | Proportion of a tract's incidents in each season | Numerical | Clustering input | Derived from START_DATE. Drop it if it adds noise |
| OFFENSE | Crime type (9 categories, such as theft, robbery, assault with a dangerous weapon) | Categorical | Classification input | Convert to per-tract offense shares. Merge ARSON (4 rows) into an "other" group |
| METHOD | Method used: GUN, KNIFE, or OTHERS | Categorical | Classification input | Convert to per-tract gun share and knife share |
| CENSUS_TRACT | Census tract identifier | Categorical | Aggregation key | Unit of analysis. Drop the 6 rows with a missing tract |
| Incident count (per tract) | Total incidents in the tract | Numerical | Contextual (filter) | Used to set a minimum number of incidents per tract (for example 50). Not a clustering feature |
| WARD, DISTRICT, PSA (Police Service Area), ANC (Advisory Neighborhood Commission), NEIGHBORHOOD_CLUSTER | Other DC geographic units | Categorical | Contextual | Used to interpret and map the clusters afterward. NEIGHBORHOOD_CLUSTER is a DC geography, unrelated to our cluster analysis |
| SHIFT | Shift label: DAY, EVENING, or MIDNIGHT | Categorical | Exclude from clustering | Assigned by report time, not incident time, so it would mix up when crimes occur and when they are reported. Used only as a cross-check |
| LATITUDE, LONGITUDE | Incident location (degrees) | Numerical | Contextual | For mapping clusters. Locations are anonymized to the block level |
| X, Y, XBLOCK, YBLOCK, BLOCK, BLOCK_GROUP, VOTING_PRECINCT, BID (Business Improvement District), END_DATE | Duplicate location fields or sparse fields | Mixed | Exclude | Redundant with other columns, or mostly missing (BID is missing for about 80% of rows) |
| CCN (Central Complaint Number), OBJECTID, OCTO_RECORD_ID | Record identifiers | Identifier | Exclude | Identifiers carry no information about crime patterns. OCTO_RECORD_ID is entirely empty. Remove duplicate CCN rows (3 homicide cases appear twice) |
| Cluster label | Cluster assignment produced later | Categorical | Classification target | Created after clustering. Never used as an input feature |

### Rationale

**How the clustering variables relate to the research question.** The question asks whether some areas have crime concentrated late at night while others are daytime-dominant. The clustering inputs (hour-of-day shares, weekend share, and seasonal share per census tract) describe when crime happens in each tract. Using proportions instead of counts means the clusters reflect timing and not how much crime a tract has.

**Candidate predictors for explaining the clusters.** The classification stage will use the per-tract offense shares (OFFENSE) and the gun and knife shares (METHOD) to predict the cluster labels. Ward, district, and the other geographic units are kept as context for interpreting and mapping the clusters. Because the predictors differ from the clustering variables, the classifier explains the clusters with independent information instead of only characterizing them. If the same variables were used for both, it would characterize the clustering result and not independently validate it.

**Variables to exclude.** Record identifiers (CCN, OBJECTID, OCTO_RECORD_ID), duplicate or redundant location fields (X, Y, XBLOCK, YBLOCK, BLOCK, BLOCK_GROUP, VOTING_PRECINCT), sparse fields (BID, END_DATE), and SHIFT, which follows report time and not incident time. The cluster label is never an input feature.

**Preparation needs.**
- **Missing values:** 6 rows have no census tract and are dropped. Duplicate case records are removed. Tracts with too few incidents are filtered out, because proportions from a handful of incidents are unreliable.
- **Time handling:** All timestamps are in UTC and are converted to Eastern time before extracting hour, weekday, and season. Only incidents that started in 2025 and were reported promptly are kept.
- **Scaling:** The clustering features are proportions, but they are standardized before dimensionality reduction and clustering.
- **Categorical encoding:** OFFENSE and METHOD are converted into per-tract shares, so no separate encoding is needed.

## 3. Supplementary Dataset

### Alcohol License Business Locations 

**Provider:** Records from Alcoholic Beverage and Cannabis Administration (ABCA)

**Link:** https://opendata.dc.gov/datasets/DCGIS::alcohol-license-business-locations/about

**Description:** This supplementary dataset from DC gives us a list of alcohol licensed businesses. It provides us with a separate measure of nightlife (where bars, nightclubs, and restaurants with entertainment are located), which helps us analyze the late-night crimes.

### Relevant Variables Table

| Relevant Variable | Description/measures | Role/Purpose |
|---|---|---|
| TYPE | What kind of establishment | Differentiates nightlife establishments from stores and restaurants. |
| ENTERTAINMENT, DANCING, COVERCHARGE | Checks off whether the establishment has any dancing, covercharge, or dancing. | Helps us distinguish places that may have entertainment (nightlife).|
| LATITUDE, LONGITUDE | Exact location | Mapping and placing the licenses in census tracts. |
| WARD, ANC, SMD | Ward, Advisory Neighborhood Commission, and single-member district | All of these are shared identifiers with the DC crime file, allows us to locate restaurants, clubs, or bars near any crimes. |


### How it could contribute to your research question or cluster interpretation

This additional dataset from the Alcoholic Beverage and Cannabis Administration:

**i.** Checks "nightlife" label. If the late-night cluster contains more nightclubs and entertainment-dominant establishments per area than daytime-dominant clusters, the label is better favored. If it doesn't, the cluster may be late-night for different reasons.

**ii.** Separates establishment types: Allows us to compare restaurants, nightclubs, and bars with off-premise stores, like liquor or grocery stores. It shows us whether late-night crimes have an association with establishments with entertainment and alcohol.

### How it could connect to your current data

**i.** ANC: Both datasets have an ANC field, which serves as a direct shared identifier. A shared identifier allows us to put each area's crime count and nightlife establish into a row, so we can compare whether areas with high late-night are also areas that contain nightclubs and bars. The formats for the values differ, but after removing the prefix ANC, all 46 ANCs in the crime file have a match. 

**ii.** Ward: DC is divided into eight wards, this is listed in each the crime and licensed business dataset. With a wider range, this allows us to evaluate the correlation of late-night crimes and establishments that contain entertainment and alcoholic beverages. Analyzing wards makes it clearer and easier to understand, we can simply see whether a ward with the most nightlife also has the most late night crime. Although eight wards may be too few for detailed analyzes and each ward combines busy nightlife and quiet areas, we can ulitize wards to quickly check on our 

---

# Future Project Updates

*Updates from later sessions will be added here.*
