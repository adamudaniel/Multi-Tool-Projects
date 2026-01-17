-- ----1. Environmental and demographic risk factors------------
-------- drinking and smoking with lesion type (good)----------
SELECT count(t1.smoke) as frequency, t2.diagnostic
FROM table1 t1
JOIN table2 t2 on t1.patient_id = t2.patient_id
where smoke = 'true' or drink = 'true'
group by t2.diagnostic
order by count(t1.smoke) desc;
------------------------------------------------------------
SELECT t1.smoke, t1.drink, count(t1.smoke) as frequency, t2.diagnostic
FROM table1 t1
JOIN table2 t2 on t1.patient_id = t2.patient_id
where smoke = 'false' and drink = 'false'
group by t1.smoke, t1.drink, t2.diagnostic
order by count(t1.smoke) desc;

-- background father, mother with skin and cancer history (good)
--first to check cancer history
SELECT t1.background_father, t1.background_mother, count(t1.background_father) as frequency, t1.skin_cancer_history, t1.cancer_history
FROM table1 t1
where t1.skin_cancer_history = 'true' and t1.cancer_history = 'true'
group by t1.background_father, t1.background_mother, t1.skin_cancer_history, t1.cancer_history
having count(t1.background_father) > 2
order by count(t1.background_father) desc;
----------------------------------------------------------
--second to check background and type of lesion
SELECT t1.background_father, t1.background_mother, 
count(t1.background_father) as frequency, t2.diagnostic
FROM table1 t1
JOIN table2 t2 on t1.patient_id = t2.patient_id
where t1.background_father <> 'UNKNOWN' and t1.background_mother <> 'UNKNOWN'
group by t1.background_father, t1.background_mother, t2.diagnostic
having count(t1.background_father) > 2
order by count(t1.background_father) desc;

--age and specific skin lesions (good)
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

--Exposure to pesticide and lesion type (good)
select t1.pesticide, count(t1.pesticide), t2.diagnostic
FROM table1 t1
JOIN table2 t2 on t1.patient_id = t2.patient_id
where pesticide = 'Yes'
group by t1.pesticide, t2.diagnostic
order by count(t1.pesticide) desc;
-----------------------------------------------------------
select t1.pesticide, count(t1.pesticide), t2.diagnostic
FROM table1 t1
JOIN table2 t2 on t1.patient_id = t2.patient_id
where pesticide = 'No'
group by t1.pesticide, t2.diagnostic
order by count(t1.pesticide) desc;

-- Gender and lesion type (good)
-- check for female
select t1.gender, count(t1.gender), t2.diagnostic
FROM table1 t1
JOIN table2 t2 on t1.patient_id = t2.patient_id
where gender = 'FEMALE'
group by t1.gender, t2.diagnostic
order by count(t1.gender) desc;
----------------------------------------------------
-- check for male
select t1.gender, count(t1.gender), t2.diagnostic
FROM table1 t1
JOIN table2 t2 on t1.patient_id = t2.patient_id
where gender = 'MALE'
group by t1.gender, t2.diagnostic
order by count(t1.gender) desc;

-- Piped water and Sewage system on lesion type (good)
--People without pipe water and sewage
select t1.has_piped_water, t1.has_sewage_system,
count(t1.has_piped_water) as frequency, t2.diagnostic
FROM table1 t1
JOIN table2 t2 on t1.patient_id = t2.patient_id
where has_piped_water = 'false' and has_sewage_system = 'false'
group by t1.has_piped_water, t1.has_sewage_system, t2.diagnostic
order by count(t1.has_piped_water) desc;
---------------------------------------------------
--People with pipe water or sewage
select t1.has_piped_water, t1.has_sewage_system,
count(t1.has_piped_water) as frequency, t2.diagnostic
FROM table1 t1
JOIN table2 t2 on t1.patient_id = t2.patient_id
where has_piped_water = 'true' and has_sewage_system = 'true'
group by t1.has_piped_water, t1.has_sewage_system, t2.diagnostic
order by count(t1.has_piped_water) desc;

-- 2. Lesion characteristics (cancerous vs.benign lesions)
-- Fitspatrick skin type with diagnostic
select fitspatrick, count(fitspatrick), diagnostic 
from table2
group by fitspatrick, diagnostic
order by fitspatrick ASC;

-- region with diagnostic
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

-- diameter 1 and 2 on diagnostic
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

--itch, grew, hurt, changed, bleed, elevation on diagnostic
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

MACHINE LEARNING DATASET
select * from table1
join table2 on table1.patient_id = table2.patient_id;

EPIDEMOLOGICAL STUDIES DATASET
select * from table2