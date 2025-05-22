\connect medica;

CREATE VIEW metformin_patients_q2_2023 AS
SELECT 
  p.patient_id,
  p.name,
  v.date,
  t.drug
FROM patients p
JOIN visits v ON p.patient_id = v.patient_id
JOIN diagnoses d ON v.visit_id = d.visit_id
JOIN treatments t ON d.diagnosis_id = t.diagnosis_id
WHERE t.drug = 'Metformin'
  AND v.date BETWEEN '2023-04-01' AND '2023-06-30';


CREATE VIEW masked_patients AS
SELECT
  patient_id,
  LEFT(name, 1) || '***' AS name
FROM patients;
