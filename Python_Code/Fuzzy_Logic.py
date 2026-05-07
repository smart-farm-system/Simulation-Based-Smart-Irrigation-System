import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import pandas as pd
import os

# ==========================================
# 1. Data Loading Section
# ==========================================
def load_data(filename='data.csv'):
    """
    Attempts to load data with specific columns.
    Returns DataFrame with columns: 'time', 'Temperature', 'soil_moisture', 'time_of_day'
    """
    df = None
    
    if os.path.exists(filename):
        try:
            try:
                df = pd.read_csv(filename)
            except:
                df = pd.read_excel(filename)
            
            # Normalize column names
            df.columns = [c.strip() for c in df.columns]
            print(f"Successfully loaded {filename}")
            
        except Exception as e:
            print(f"File found but could not be read: {e}")

    # Expected column mapping
    expected_cols = {
        'time': 'time',
        'temperature': 'Temperature', 
        'soil_moisture': 'soil_moisture', 
        'time_of_day': 'time_of_day'
    }

    if df is not None:
        col_map = {c.lower(): c for c in df.columns}
        missing = []
        for req_lower in ['temperature', 'soil_moisture', 'time_of_day']:
            if req_lower not in col_map:
                missing.append(expected_cols[req_lower])
        
        if missing:
            print(f"Missing columns: {missing}. Switching to synthetic data.")
            df = None
        else:
            # Rename columns
            rename_dict = {
                col_map['temperature']: 'Temperature',
                col_map['soil_moisture']: 'soil_moisture',
                col_map['time_of_day']: 'time_of_day'
            }
            if 'time' in col_map:
                rename_dict[col_map['time']] = 'time'
            
            df = df.rename(columns=rename_dict)
            if 'time' not in df.columns:
                df['time'] = np.arange(len(df))

    # Fallback: Synthetic Data
    if df is None:
        print("Using synthetic data for simulation...")
        t_steps = 144
        time_vals = np.linspace(0, 24, t_steps)
        df = pd.DataFrame({
            'time': time_vals,
            'time_of_day': time_vals % 24,
            'Temperature': np.full(t_steps, 25) + 5 * np.sin(time_vals/24 * 2*np.pi),
            'soil_moisture': 50 + 30 * np.sin(2 * np.pi * np.linspace(0, 1, t_steps))
        })
    
    return df

df = load_data('data.csv')

# ==========================================
# 2. Fuzzy Variables Setup
# ==========================================
temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'Temperature')
soil_moisture = ctrl.Antecedent(np.arange(0, 101, 1), 'soil_moisture')
time_of_day = ctrl.Antecedent(np.arange(0, 25, 1), 'time_of_day')
irrigation = ctrl.Consequent(np.arange(0, 101, 1), 'irrigation_intensity')

# Membership functions
temperature['cold'] = fuzz.trimf(temperature.universe, [0, 0, 15])
temperature['moderate'] = fuzz.trimf(temperature.universe, [10, 20, 30])
temperature['hot'] = fuzz.trimf(temperature.universe, [25, 40, 40])

soil_moisture['dry'] = fuzz.trimf(soil_moisture.universe, [0, 0, 40])
soil_moisture['optimal'] = fuzz.trimf(soil_moisture.universe, [30, 50, 70])
soil_moisture['wet'] = fuzz.trimf(soil_moisture.universe, [60, 100, 100])

time_of_day['night'] = fuzz.trimf(time_of_day.universe, [0, 0, 6])
time_of_day['morning'] = fuzz.trimf(time_of_day.universe, [5, 8, 11])
time_of_day['noon'] = fuzz.trimf(time_of_day.universe, [10, 13, 16])
time_of_day['evening'] = fuzz.trimf(time_of_day.universe, [15, 20, 24])

irrigation['low'] = fuzz.trimf(irrigation.universe, [0, 0, 40])
irrigation['medium'] = fuzz.trimf(irrigation.universe, [30, 50, 70])
irrigation['high'] = fuzz.trimf(irrigation.universe, [60, 100, 100])

# Rules
rules = [
    ctrl.Rule(temperature['hot'] & soil_moisture['dry'] & time_of_day['morning'], irrigation['high']),
    ctrl.Rule(temperature['hot'] & soil_moisture['dry'] & time_of_day['noon'], irrigation['medium']),
    ctrl.Rule(temperature['moderate'] & soil_moisture['dry'], irrigation['medium']),
    ctrl.Rule(soil_moisture['wet'], irrigation['low']),
    ctrl.Rule(soil_moisture['optimal'], irrigation['low']),
    ctrl.Rule(temperature['cold'], irrigation['low']),
    ctrl.Rule(time_of_day['night'], irrigation['low']),
    ctrl.Rule(time_of_day['evening'], irrigation['low']),
]

system = ctrl.ControlSystem(rules)
sim = ctrl.ControlSystemSimulation(system)

# ==========================================
# 3. Compute Logic for Data
# ==========================================
results = []
for index, row in df.iterrows():
    sim.input['Temperature'] = row['Temperature']
    sim.input['soil_moisture'] = row['soil_moisture']
    sim.input['time_of_day'] = row['time_of_day']
    sim.compute()
    results.append(sim.output['irrigation_intensity'])

df['irrigation_intensity'] = results

# ==========================================
# 4. Generate All Graphs
# ==========================================

# --- Graphs 1-4: Membership Functions ---
# We loop through them to generate individual plots for each variable
variables = [temperature, soil_moisture, time_of_day, irrigation]
labels = ['Temperature', 'Soil Moisture', 'Time of Day', 'Irrigation Intensity']

for var, label in zip(variables, labels):
    plt.figure(figsize=(7, 4))
    var.view()
    plt.title(f'Membership functions for {label}')
    plt.tight_layout()
    plt.show()

# --- Graph 5: 3D Surface Plot (Theoretical) ---
soil_vals = np.linspace(0, 100, 50)
temp_vals = np.linspace(0, 40, 50)
X, Y = np.meshgrid(soil_vals, temp_vals)
Z = np.zeros_like(X)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        sim.input['soil_moisture'] = X[i, j]
        sim.input['Temperature'] = Y[i, j]
        sim.input['time_of_day'] = 8  # Fixed morning
        sim.compute()
        Z[i, j] = sim.output['irrigation_intensity']

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
ax.set_xlabel('Soil Moisture [%]')
ax.set_ylabel('Temperature [°C]')
ax.set_zlabel('Irrigation Intensity')
ax.set_title('Fuzzy Control Surface (Morning)')
plt.show()

# --- Graph 6: 2D Contour Plot ---
plt.figure(figsize=(8, 6))
contour = plt.contourf(X, Y, Z, 20, cmap='plasma')
plt.xlabel('Soil Moisture [%]')
plt.ylabel('Temperature [°C]')
plt.title('Fuzzy Controller Output (Contour, Morning)')
cbar = plt.colorbar(contour)
cbar.set_label('Irrigation Intensity')
plt.tight_layout()
plt.show()

# --- Graph 7: Water Propagation Heatmap (Using Loaded Data) ---
depth = np.linspace(0, 1200, 100)
soil_humidity = np.zeros((len(depth), len(df)))

for t_idx, intensity in enumerate(df['irrigation_intensity']):
    soil_humidity[:, t_idx] = intensity * np.exp(-depth/400)

plt.figure(figsize=(10, 5))
# Determine extent for x-axis
if pd.api.types.is_numeric_dtype(df['time']):
    extent = [df['time'].min(), df['time'].max(), 0, 1200]
    xlabel = 'Time'
else:
    extent = [0, len(df), 0, 1200]
    xlabel = 'Sample Index'

plt.imshow(soil_humidity, aspect='auto', origin='lower',
           extent=extent, cmap='Blues', vmin=0, vmax=100)
plt.colorbar(label='Soil Humidity [%]')
plt.xlabel(xlabel)
plt.ylabel('Depth [mm]')
plt.title('Distribution of Water Propagation in Soil')
plt.show()

# --- Graph 8: Irrigation Intensity Over Time (Using Loaded Data) ---
plt.figure(figsize=(10, 4))
plt.plot(df['time'], df['irrigation_intensity'], label='Calculated Intensity', color='tab:blue', linewidth=2)
plt.xlabel('Time')
plt.ylabel('Irrigation Intensity')
plt.title('Irrigation Intensity over Time')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# --- Graph 9: Histogram of Irrigation Intensity (Using Loaded Data) ---
plt.figure(figsize=(8, 4))
plt.hist(df['irrigation_intensity'], bins=20, color='teal', edgecolor='black')
plt.xlabel('Irrigation Intensity')
plt.ylabel('Frequency')
plt.title('Histogram of Irrigation Intensity')
plt.tight_layout()
plt.show()