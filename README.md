# Solar-Powered IoT-Based Smart Irrigation System with Fuzzy Logic Control

This repository contains the simulation source code, hardware schematics and data visualization scripts for an autonomous smart irrigation system. The architecture utilizes a Mamdani-style Fuzzy Inference System (FIS) to dynamically calculate optimal irrigation intensity based on real-time environmental variables, effectively minimizing water waste and energy consumption.

## 📌 Project Architecture

This project is divided into two primary environments:
1. **Hardware Simulation (Arduino/Proteus):** Implements the embedded fuzzy logic controller using the `eFLL` library to actuate a water pump via PWM based on soil moisture, temperature, and time of day.
2. **Data Analysis & Visualization (Python):** Utilizes `scikit-fuzzy` to process simulated datasets (Virtual Terminal output), validate the control logic, and generate academic-grade visualizations (Membership Functions, 3D Control Surfaces, Heatmaps).

## 🗂️ Repository Structure

<img width="765" height="446" alt="image" src="https://github.com/user-attachments/assets/643ac6e6-b005-4f22-aa29-b3dd8c8228af" />

## 🗂️ Repository Structure

```text
├── arduino/
│   └── Smart_Irrigation_Fuzzy/
│       └── Smart_Irrigation_Fuzzy.ino   # Main embedded C++ code for Arduino
├── python/
│   ├── fuzzy_analysis.py                # Python script for generating graphs and validating logic
│   └── data.csv                         # Sample dataset generated from Proteus Virtual Terminal
├── proteus/
│   └── Smart_Irrigation_Schematic.pdsprj # Proteus simulation project file
└── README.md 
