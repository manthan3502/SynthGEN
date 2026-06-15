# SynthGEN – AI-Powered Synthetic Data Generator

## Overview

SynthGEN is a full-stack web application that generates realistic synthetic datasets for analytics, software testing, and development purposes.

The platform combines Google Gemini API and Faker to automatically generate structured synthetic data based on user-defined requirements.

---

## Features

* Generate realistic synthetic datasets
* AI-assisted metadata generation using Google Gemini API
* Export data in CSV and JSON formats
* Store generation history using SQLite
* Simple and interactive web interface

---

## Tech Stack

### Frontend

* React
* Vite
* Tailwind CSS
* Axios

### Backend

* FastAPI
* Python
* Uvicorn
* Pydantic

### Database

* SQLite

### AI & Data Generation

* Google Gemini API
* Faker
* Pandas

---

## Workflow

1. User selects required fields.
2. Frontend sends configuration to backend.
3. Gemini API generates metadata configuration.
4. Faker generates synthetic records.
5. Dataset is exported in CSV or JSON format.

---

## Project Structure

Frontend (React)
↓
FastAPI Backend
↓
Gemini API Metadata Generation
↓
Faker Data Generation
↓
SQLite History Storage
↓
CSV / JSON Export

---

## Future Improvements

* User authentication
* Cloud deployment
* Dataset templates
* More export formats
* Advanced data generation controls

---

## Author

Manthan Karekar

B.Tech Computer Science Engineering

DES Pune University
