CREATE DATABASE medica;

\connect medica;

CREATE TABLE patients (
  patient_id VARCHAR PRIMARY KEY,
  name TEXT
);

CREATE TABLE visits (
  visit_id VARCHAR PRIMARY KEY,
  patient_id VARCHAR ,
  date DATE,
  provider_notes_text TEXT,
  provider_notes_author TEXT
);

CREATE TABLE diagnoses (
  diagnosis_id VARCHAR PRIMARY KEY,
  visit_id VARCHAR ,
  code VARCHAR,
  description TEXT
);

CREATE TABLE treatments (
  treatment_id VARCHAR PRIMARY KEY,
  diagnosis_id VARCHAR ,
  drug VARCHAR,
  dose VARCHAR
);
