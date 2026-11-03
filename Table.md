## Variable-Selection Table

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
