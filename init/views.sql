\connect medica;

CREATE VIEW masked_patients AS
SELECT
  patient_id,
  LEFT(name, 1) || '***' AS name
FROM patients;

CREATE VIEW metformin_patients_q2_2023 AS
SELECT 
  p.patient_id,
  p.name,
  v.date,
  t.drug
FROM masked_patients p
JOIN visits v ON p.patient_id = v.patient_id
JOIN diagnoses d ON v.visit_id = d.visit_id
JOIN treatments t ON d.diagnosis_id = t.diagnosis_id
WHERE t.drug = 'Metformin'
AND v.date BETWEEN '2023-04-01' AND '2023-06-30';

CREATE ROLE bi_user WITH LOGIN PASSWORD 'bi_pass';
GRANT CONNECT ON DATABASE medica TO bi_user;
GRANT USAGE ON SCHEMA public TO bi_user;
GRANT SELECT ON  treatments, diagnoses, visits, metformin_patients_q2_2023, masked_patients TO bi_user;


