## Research Question: Are there "nightlife" type areas where crime concentrates late at night, and how do they differ from areas with daytime-dominant crime

## Boston Crime Report

**Provider:** Boston Police Department, issued by the City of Boston Department of Innovation and Technology.

**Link:** https://data.boston.gov/dataset/crime-incident-reports-august-2015-to-date-source-new-system

## Relevant Variables Table

| Boston Variable | Description | DC Correlation | Role/Purpose |
|---|---|---|---|
| OCCURRED_ON_DATE | Date and time the incident could have taken place. | START_DATE | Used to define night-time and daytime. We turn it into each subdivision: late-night, evening, and daytime, so that it groups by when crimes occur. Also lets us label the resulting clusters (nightlife vs. daytime dominant) and compare their timing in DC and Boston. |
| OFFENSE_CODE, OFFENSE_DESCRIPTION | Category and seriousness of the offense | OFFENSE | Classification inputs are matched to DC's groups; OFFENSE_DESCRIPTION ensures accurate comparison of offenses. |
| DISTRICT, REPORTING_AREA | Which part the crime is located in. | DISTRICT, PSA | Describes where each cluster occurred.|
| HOUR, DAY_OF_WEEK, MONTH | Cluster of the day, month, and hour occurred. | START_DATE | DAY_OF_WEEK measures weekend-night share, which separates actual nightlife areas from areas that are busy late on weeknights for different reasons. We utilize these to cross-check if there are any time mistakes. |
| SHOOTING | Whether shootings were involved in the crime. | METHOD | Measures how severe crime may be in each section. Helps answer whether late-night clusters are more violent. Closely related to the DC gun share, but is not identical. |


## How it could contribute to your research question or cluster interpretation.
This additional dataset from Boston adds:

**i.** Comparative test: Finding a nightlife cluster in DC may demonstrate something specific to DC. But if a similar and comparable city, like Boston, also creates a group of clusters with unusually high late-night crimes, it may support the idea that nightlife areas are a recognizable pattern.

**ii.** Interpretation: If nightlife clusters in both cities display an offense profile that varies from the daytime-dominant cluster, the interpretation is likely to be more convincing. For instance, we hypothesize that late-night clusters have a larger number of violent crimes and daytime clusters has a less amount of crimes. If similar patterns appear in Boston, this could strengthen our interpretation. However, if DC and Boston disagree, then that points to city-specific factors, like differing regulations and areas.

## How it could connect to your current data—for example, through a shared identifier, location, or time period.

**i.** Shared Features: Both cities' datasets include similar features that have the same definitions, including when crimes occurred, types of offenses, and their geographic locations. Only 2025 crime incidents are used to sustain a consistent time period.  Timestamps are converted into Eastern local time, considering both Eastern Standard Time and Eastern Daylight Time, before creating standardized time variables like hour, day, and month.

**ii.** Offense Classification:  Boston's OFFENSE_CODE and OFFENSE_DESCRIPTION are used to help group offenses into categories, like violent, property, and other crimes. Similarly, Washington, D.C.'s OFFENSE variable can be used to create comparable offense categories. This allows us to analyze whether varying methods of crime are correlated with nighttime and daytime dominant zones in both cities.

**iii.** Geographic: Both datasets hold different geographic identifiers. Washington, D.C., uses census tracts (small subdivisions of a county), while Boston provides reporting areas and police districts. Even though these geographic units can't be directly the same, we can examine each city independently and compare the resulting crime pattern at its own geographic level.

