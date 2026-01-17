-- QUESTION 1
--------ENVIRONMAENTAL & DEMOGRAPHIC FACTORS--------------
-------- drinking and smoking with lesion type (good)----------
---People that have either drank or smoked
SELECT
    T1.drink, T1.smoke,
    SUM(CASE
        WHEN T2.diagnostic IN ('MEL', 'SCC', 'BCC') THEN 1
        ELSE 0
    END) AS Cancerous_Count,
    
    SUM(CASE
        WHEN T2.diagnostic IN ('SEK', 'NEV') THEN 1
        ELSE 0
    END) AS Noncancerous_Count,
	sum(CASE
		WHEN T2.diagnostic IN ('ACK') THEN 1 
		ELSE 0
	END) AS Precancerous_Count, 
    COUNT(T2.diagnostic) AS Total_Diagnoses
FROM
    table1 AS T1
JOIN
    table2 AS T2 ON T1.patient_id = T2.patient_id
WHERE T1.drink = 'true' OR T1.smoke ='true'
GROUP BY
    T1.drink, T1.smoke
ORDER BY
    T1.drink;
	
---People that have never drink or smoke
SELECT
    T1.drink, T1.smoke,
    SUM(CASE
        WHEN T2.diagnostic IN ('MEL', 'SCC', 'BCC') THEN 1
        ELSE 0
    END) AS Cancerous_Count,
    
    SUM(CASE
        WHEN T2.diagnostic IN ('SEK', 'NEV') THEN 1
        ELSE 0
    END) AS Noncancerous_Count,
	sum(CASE
		WHEN T2.diagnostic IN ('ACK') THEN 1 
		ELSE 0
	END) AS Precancerous_Count, 
    COUNT(T2.diagnostic) AS Total_Diagnoses
FROM
    table1 AS T1
JOIN
    table2 AS T2 ON T1.patient_id = T2.patient_id
WHERE T1.drink = 'false' AND T1.smoke ='false'
GROUP BY
    T1.drink, T1.smoke
ORDER BY
    T1.drink;

------------------- ETHNIC BACKGROUND VRS CANCERS  ------------------------
-- Common backgrounds that have cancer and skin cancer history
SELECT t1.background_father, t1.background_mother, count(t1.background_father) as frequency, t1.skin_cancer_history, t1.cancer_history
FROM table1 t1
where t1.skin_cancer_history = 'true' and t1.cancer_history = 'true'
group by t1.background_father, t1.background_mother, t1.skin_cancer_history, t1.cancer_history
having count(t1.background_father) > 2
order by count(t1.background_father) desc;	

-- backgrouns with diagnosis (filtering out 'Unknown')
SELECT t1.background_father, t1.background_mother, 
count(t1.background_father) as frequency, t2.diagnostic
FROM table1 t1
JOIN table2 t2 on t1.patient_id = t2.patient_id
where t1.background_father <> 'UNKNOWN' and t1.background_mother <> 'UNKNOWN'
group by t1.background_father, t1.background_mother, t2.diagnostic
having count(t1.background_father) > 2
order by count(t1.background_father) desc; 

-------------------------------- AGE CATEGORY ---------------------------------------------
-- Cancer type and the average age of people affected
SELECT avg(t1.age) as avg_age, count(age) as frequency, t2.diagnostic,
	SUM(CASE WHEN T2.diagnostic IN ('MEL', 'SCC', 'BCC') THEN 1
        ELSE 0
    END) AS Cancerous_Count,
    
    SUM(CASE WHEN T2.diagnostic IN ('SEK', 'NEV') THEN 1
        ELSE 0
    END) AS Noncancerous_Count,
	
	sum(CASE WHEN T2.diagnostic IN ('ACK') THEN 1 
		ELSE 0
	END) AS Precancerous_Count, 
    
	COUNT(T2.diagnostic) AS Total_Diagnoses
FROM table1 t1
JOIN table2 t2 on t1.patient_id = t2.patient_id
group by t2.diagnostic;

-- Exposure to pesticide and correlation to cancer type
SELECT
     T1.pesticide,
    SUM(CASE
        WHEN T2.diagnostic IN ('MEL', 'SCC', 'BCC') THEN 1
        ELSE 0
    END) AS Cancerous_Count,
    
    SUM(CASE
        WHEN T2.diagnostic IN ('SEK', 'NEV') THEN 1
        ELSE 0
    END) AS Noncancerous_Count,
	sum(CASE
		WHEN T2.diagnostic IN ('ACK') THEN 1 
		ELSE 0
	END) AS Precancerous_Count, 
    COUNT(T2.diagnostic) AS Total_Diagnoses
FROM
    table1 AS T1
JOIN
    table2 AS T2 ON T1.patient_id = T2.patient_id
WHERE T1.pesticide='true' OR T1.pesticide ='false'
GROUP BY
       T1.pesticide
ORDER BY
    T1.pesticide;

----------------------- GENDER VRS SKIN CANCERS ----------------- 
-- Common cancer type based on gender group
SELECT
    T1.gender,
    SUM(CASE
        WHEN T2.diagnostic IN ('MEL', 'SCC', 'BCC') THEN 1
        ELSE 0
    END) AS Cancerous_Count,
    
    SUM(CASE
        WHEN T2.diagnostic IN ('SEK', 'NEV') THEN 1
        ELSE 0
    END) AS Noncancerous_Count,
	sum(CASE
		WHEN T2.diagnostic IN ('ACK') THEN 1 
		ELSE 0
	END) AS Precancerous_Count, 
    COUNT(T2.diagnostic) AS Total_Diagnoses
FROM
    table1 AS T1
JOIN
    table2 AS T2 ON T1.patient_id = T2.patient_id
GROUP BY
    T1.gender
ORDER BY
    T1.gender;

------------------------ Pipe water or sewage --------------------
--People using either of pipe water or sewage system
SELECT
     T1.has_piped_water, T1.has_sewage_system,
    SUM(CASE
        WHEN T2.diagnostic IN ('MEL', 'SCC', 'BCC') THEN 1
        ELSE 0
    END) AS Cancerous_Count,
    
    SUM(CASE
        WHEN T2.diagnostic IN ('SEK', 'NEV') THEN 1
        ELSE 0
    END) AS Noncancerous_Count,
	sum(CASE
		WHEN T2.diagnostic IN ('ACK') THEN 1 
		ELSE 0
	END) AS Precancerous_Count, 
    COUNT(T2.diagnostic) AS Total_Diagnoses
FROM
    table1 AS T1
JOIN
    table2 AS T2 ON T1.patient_id = T2.patient_id
WHERE  T1.has_piped_water ='true' OR T1.has_sewage_system = 'true'
GROUP BY
       T1.has_piped_water, T1.has_sewage_system
ORDER BY
    T1.has_piped_water;

--People who don't have pipe water nor sewage system
SELECT
     T1.has_piped_water, T1.has_sewage_system,
    SUM(CASE
        WHEN T2.diagnostic IN ('MEL', 'SCC', 'BCC') THEN 1
        ELSE 0
    END) AS Cancerous_Count,
    
    SUM(CASE
        WHEN T2.diagnostic IN ('SEK', 'NEV') THEN 1
        ELSE 0
    END) AS Noncancerous_Count,
	sum(CASE
		WHEN T2.diagnostic IN ('ACK') THEN 1 
		ELSE 0
	END) AS Precancerous_Count, 
    COUNT(T2.diagnostic) AS Total_Diagnoses
FROM
    table1 AS T1
JOIN
    table2 AS T2 ON T1.patient_id = T2.patient_id
WHERE  T1.has_piped_water ='false' AND T1.has_sewage_system = 'false'
GROUP BY
       T1.has_piped_water, T1.has_sewage_system
ORDER BY
    T1.has_piped_water;


-- QUESTION 2
---------------lESION CHARACTERISTIC ON CANCER TYPE------------------ 
-------  Fitspatrick skin type and common cancer type  --------------------------
SELECT
    fitspatrick,
    SUM(CASE
        WHEN diagnostic IN ('MEL', 'SCC', 'BCC') THEN 1
        ELSE 0
    END) AS Cancerous_Count,
    
    SUM(CASE
        WHEN diagnostic IN ('SEK', 'NEV') THEN 1
        ELSE 0
    END) AS Noncancerous_Count,
	sum(CASE
		WHEN diagnostic IN ('ACK') THEN 1 
		ELSE 0
	END) AS Precancerous_Count, 
    COUNT(diagnostic) AS Total_Diagnoses
FROM
    table2
GROUP BY
    fitspatrick
ORDER BY
	fitspatrick ASC;

----------------- REGION VRS SKIN CANCERS -------------------
-- What cancer type typically grows a region of the body
select region, count(region) as frequency, diagnostic,
	SUM(CASE WHEN diagnostic IN ('MEL', 'SCC', 'BCC') THEN 1
        ELSE 0
    END) AS Cancerous_Count,
    
    SUM(CASE WHEN diagnostic IN ('SEK', 'NEV') THEN 1
        ELSE 0
    END) AS Noncancerous_Count,
	sum(CASE WHEN diagnostic IN ('ACK') THEN 1 
		ELSE 0
	END) AS Precancerous_Count, 
    COUNT(diagnostic) AS Total_Diagnoses
from table2
group by region, diagnostic
having count(region) > 2
order by region ASC;

-------------------- DIAMETER VRS SKIN CANCERS -------------------
-- What diameters are the type of cancers
select diameter_1, diameter_2, count(diameter_1) as frequency, diagnostic,
	SUM(CASE WHEN diagnostic IN ('MEL', 'SCC', 'BCC') THEN 1
        ELSE 0
    END) AS Cancerous_Count,
    
    SUM(CASE WHEN diagnostic IN ('SEK', 'NEV') THEN 1
        ELSE 0
    END) AS Noncancerous_Count,
	sum(CASE WHEN diagnostic IN ('ACK') THEN 1 
		ELSE 0
	END) AS Precancerous_Count, 
    COUNT(diagnostic) AS Total_Diagnoses
from table2
group by diameter_1, diameter_2, diagnostic
order by count(diameter_1) desc
LIMIT 40;

--------ITCH, GREW, HURT, CHANGED, BLEED, ELEVATION VRS SKIN CANCERS --------------
-- Cancerous
select itch, grew, hurt, changed, bleed, elevation, count(diagnostic) AS Cancerous
from table2
where diagnostic = 'BCC' or diagnostic = 'SCC' or diagnostic = 'MEL'
group by itch, grew, hurt, changed, bleed, elevation
order by count(diagnostic) desc
limit 27;

-- Non-cancerous
select itch, grew, hurt, changed, bleed, elevation, count(diagnostic) AS Non_cancerous
from table2
where diagnostic = 'NEV' or diagnostic = 'SEK'
group by itch, grew, hurt, changed, bleed, elevation
order by count(diagnostic) desc
limit 11;

-- Pre-cancerous
select itch, grew, hurt, changed, bleed, elevation, count(diagnostic) AS Pre_cancerous
from table2
where diagnostic = 'ACK'
group by itch, grew, hurt, changed, bleed, elevation
order by count(diagnostic) desc
limit 17;


-- QUESTION 3
------------MACHINE LEARNING DATASET------------
--The dataset to train a machine model on skin cancer detection
--Joint dataset of table1 and table2
select * from table1
join table2 on table1.patient_id = table2.patient_id;


-- QUESTION 4
----------EPIDEMOLOGICAL STUDIES DATASET-----------
-- Table2 only
select * from table2
