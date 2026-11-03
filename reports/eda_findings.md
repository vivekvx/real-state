# EDA findings

Dataset: 250,000 listings, 20 states, 42 cities, no missing cells or duplicates. Supplied price/sqft values were inconsistent, so recomputed using price in lakhs × 100,000 / area.

### 1. Price distribution

Median ₹253.87L; middle 50% ₹132.55L–₹376.88L; right tail reaches ₹500.00L.

### 2. Size distribution

Median 2,747 sq ft; middle 50% 1,623–3,874 sq ft.

### 3. Price per sq ft by property type

Property_Type
Independent House    9305.0
Apartment            9245.0
Villa                9190.0

### 4. Size vs price

Pearson correlation = -0.003.

### 5. Outliers

IQR fences flag 19,723 price/sqft rows and 0 size rows.

### 6. Average price per sq ft by state

State
Karnataka         13252.0
Andhra Pradesh    13202.0
Uttar Pradesh     13143.0
Tamil Nadu        13132.0
Telangana         13093.0
Gujarat           13091.0
Assam             13084.0
Maharashtra       13070.0
Madhya Pradesh    13069.0
Haryana           13069.0
West Bengal       13061.0
Bihar             13051.0
Odisha            13033.0
Chhattisgarh      13027.0
Uttarakhand       13027.0
Kerala            12982.0
Jharkhand         12975.0
Delhi             12941.0
Rajasthan         12932.0
Punjab            12931.0

### 7. Average price by city (top 10)

City
Bangalore     258.46
Surat         258.08
Kochi         257.42
Gaya          257.05
Mangalore     256.92
Dehradun      256.89
Mysore        256.85
Chennai       256.83
Hyderabad     256.59
Coimbatore    256.50

### 8. Median property age by locality

Locality
Locality_443    17.0
Locality_468    18.0
Locality_312    18.0
Locality_46     18.0
Locality_13     18.0
Locality_458    18.0
Locality_92     18.0
Locality_454    18.0
Locality_290    18.0
Locality_450    18.0

Lowest ten locality medians shown; full locality summary is in `locality_age.csv`.

### 9. BHK by city

City,1,2,3,4,5
Ahmedabad,1264,1267,1272,1258,1350
Amritsar,1284,1239,1234,1224,1240
Bangalore,839,823,802,833,847
Bhopal,1238,1235,1255,1259,1297
Bhubaneswar,1236,1293,1299,1217,1278
Bilaspur,1210,1252,1275,1268,1258
Chennai,1263,1232,1183,1257,1233
Coimbatore,1236,1301,1317,1345,1262
Cuttack,1320,1292,1301,1236,1209
Dehradun,1238,1297,1225,1248,1226
Durgapur,1311,1259,1287,1260,1270
Dwarka,1295,1211,1248,1216,1276
Faridabad,1202,1231,1261,1214,1261
Gaya,1356,1259,1146,1179,1230
Gurgaon,1241,1221,1239,1232,1212
Guwahati,1240,1158,1272,1188,1234
Haridwar,1233,1290,1230,1223,1291
Hyderabad,1190,1312,1256,1271,1244
Indore,1264,1213,1218,1245,1227
Jaipur,1228,1262,1237,1277,1227
Jamshedpur,1274,1221,1324,1273,1243
Jodhpur,1254,1233,1244,1181,1259
Kochi,1270,1268,1207,1280,1280
Kolkata,1254,1267,1236,1201,1277
Lucknow,1280,1284,1259,1194,1220
Ludhiana,1283,1202,1294,1230,1286
Mangalore,826,827,783,835,792
Mumbai,818,810,871,838,812
Mysore,865,832,834,862,824
Nagpur,841,803,848,815,853
New Delhi,1297,1184,1300,1281,1244
Noida,1253,1257,1251,1193,1317
Patna,1250,1210,1189,1266,1284
Pune,902,814,842,832,834
Raipur,1206,1279,1249,1240,1219
Ranchi,1234,1216,1205,1240,1250
Silchar,1241,1255,1324,1248,1336
Surat,1269,1182,1268,1248,1200
Trivandrum,1270,1203,1299,1185,1225
Vijayawada,1204,1288,1292,1335,1225
Vishakhapatnam,1162,1255,1189,1315,1197
Warangal,1255,1278,1202,1246,1285


### 10. Price trends in top five localities

Locality
Locality_395    275.43
Locality_366    273.41
Locality_497    270.00
Locality_360    269.81
Locality_203    269.03

No date or time series exists, so these are price levels, not trends.

### 11. Numeric correlations

                        BHK  Size_in_SqFt  Price_in_Lakhs  Price_per_SqFt  Year_Built  Age_of_Property  Floor_No  Total_Floors  Nearby_Schools  Nearby_Hospitals  School_Density_Score  Hospital_Density_Score
BHK                     1.0         -0.00           -0.00            0.00         0.0             -0.0       0.0         -0.00           -0.00              0.00                  0.00                    0.00
Size_in_SqFt           -0.0          1.00           -0.00           -0.61         0.0             -0.0      -0.0         -0.00            0.00             -0.00                 -0.63                   -0.63
Price_in_Lakhs         -0.0         -0.00            1.00            0.56         0.0             -0.0      -0.0          0.00            0.00             -0.00                  0.00                    0.00
Price_per_SqFt          0.0         -0.61            0.56            1.00        -0.0              0.0      -0.0          0.00           -0.00             -0.00                  0.55                    0.55
Year_Built              0.0          0.00            0.00           -0.00         1.0             -1.0      -0.0          0.00           -0.00             -0.00                 -0.00                   -0.00
Age_of_Property        -0.0         -0.00           -0.00            0.00        -1.0              1.0       0.0         -0.00            0.00              0.00                  0.00                    0.00
Floor_No                0.0         -0.00           -0.00           -0.00        -0.0              0.0       1.0          0.00           -0.00              0.00                  0.00                    0.00
Total_Floors           -0.0         -0.00            0.00            0.00         0.0             -0.0       0.0          1.00           -0.00             -0.01                  0.00                   -0.00
Nearby_Schools         -0.0          0.00            0.00           -0.00        -0.0              0.0      -0.0         -0.00            1.00             -0.00                  0.54                   -0.00
Nearby_Hospitals        0.0         -0.00           -0.00           -0.00        -0.0              0.0       0.0         -0.01           -0.00              1.00                 -0.00                    0.54
School_Density_Score    0.0         -0.63            0.00            0.55        -0.0              0.0       0.0          0.00            0.54             -0.00                  1.00                    0.55
Hospital_Density_Score  0.0         -0.63            0.00            0.55        -0.0              0.0       0.0         -0.00           -0.00              0.54                  0.55                    1.00

### 12. Nearby schools vs price/sqft

Pearson correlation = -0.000.

### 13. Nearby hospitals vs price/sqft

Pearson correlation = -0.000.

### 14. Price by furnished status

Furnished_Status
Furnished         254.45
Semi-furnished    254.33
Unfurnished       254.98

### 15. Price/sqft by facing

Facing
West     13140.0
South    13044.0
North    13025.0
East     13024.0

### 16. Properties by owner type

Owner_Type
Broker     83479
Owner      83268
Builder    83253

### 17. Properties by availability

Availability_Status
Under_Construction    125035
Ready_to_Move         124965

### 18. Parking and price

Parking_Space
No     254.43
Yes    254.75

### 19. Amenities and price/sqft

Amenity_Count
1    13015.0
2    13059.0
3    13044.0
4    13071.0
5    13102.0

### 20. Public transport vs price/sqft

Public_Transport_Accessibility
High      13027.0
Low       13086.0
Medium    13062.0

## Interpret with care

No date field exists, so time trends cannot be inferred; no crime, infrastructure, or RERA fields exist. These are cross-sectional associations, not causal effects. Investment and future-price targets are proxy definitions documented in `target_assumptions.json`. Figures are in `figures/`.