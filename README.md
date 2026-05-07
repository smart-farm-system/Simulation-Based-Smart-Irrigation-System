# Solar-Powered IoT-Based Smart Irrigation System with Fuzzy Logic Control

This repository contains the simulation source code, hardware schematics and data visualization scripts for an autonomous smart irrigation system. The architecture utilizes a Mamdani-style Fuzzy Inference System (FIS) to dynamically calculate optimal irrigation intensity based on real-time environmental variables, effectively minimizing water waste and energy consumption.

## 📌 Project Architecture

This project is divided into two primary environments:
1. **Hardware Simulation (Arduino/Proteus):** Implements the embedded fuzzy logic controller using the `eFLL` library to actuate a water pump via PWM based on soil moisture, temperature, and time of day.
2. **Data Analysis & Visualization (Python):** Utilizes `scikit-fuzzy` to process simulated datasets (Virtual Terminal output), validate the control logic, and generate academic-grade visualizations (Membership Functions, 3D Control Surfaces, Heatmaps).

## 🗂️ Proteus Structure

<img width="765" height="446" alt="image" src="https://github.com/user-attachments/assets/643ac6e6-b005-4f22-aa29-b3dd8c8228af" />

⚙️ Prerequisites and Dependencies
For the Hardware Simulation:
Arduino IDE (v1.8.x or v2.x)

eFLL (Embedded Fuzzy Logic Library): Install via the Arduino Library Manager (Search "eFLL" by Ajax).

Proteus Professional (for .pdsprj schematic simulation).

For the Python Data Analysis:
Python 3.8+

Required Python Packages:

Bash
pip install numpy pandas scikit-fuzzy matplotlib openpyxl
🚀 How to Run the Simulation
Phase 1: Proteus & Arduino Hardware Simulation
Open Smart_Irrigation_Fuzzy.ino in the Arduino IDE.

Verify your board is set to Arduino UNO.

Compile the code and export the binary (Sketch -> Export compiled Binary). This generates a .hex file.

Open the Proteus schematic (.pdsprj).

Double-click the Arduino UNO component, locate the Program File property, and link it to the newly generated .hex file.

Hardware Note: Ensure the pump/motor driver is connected to a PWM-capable pin (e.g., Digital Pin 3), not a standard binary pin.

Run the simulation. The Virtual Terminal will output a CSV-formatted data stream of the environmental variables and calculated irrigation intensity.

Phase 2: Python Data Visualization
Copy the CSV output from the Proteus Virtual Terminal and save it as data.csv inside the /python directory.

Run the analysis script:

Bash
python fuzzy_analysis.py
The script will ingest the hardware simulation data and automatically generate the following plots:

Figures 2-5: Triangular Membership Functions (Temperature, Soil Moisture, Time of Day, Irrigation Intensity).

Figure 6 & 7: 3D Surface Plot and 2D Contour Map of the Fuzzy Control Logic.

Figure 8 & 9: Time Series and Frequency Histogram of the Irrigation Intensity.

Figure 10: 2D Heatmap of Water Propagation in the soil profile.

🧠 Fuzzy Logic Rule Base
The core decision engine relies on a 36-rule Mamdani inference system. It evaluates three continuous inputs:

Soil Moisture: Dry, Optimal, Wet

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
Temperature: Cold, Moderate, Hot

Time of Day: Morning, Noon, Evening, Night
