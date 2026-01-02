# 🚦 Traffic Data Analysis & Histogram Visualization (Python + Tkinter)

This project analyzes vehicle traffic data from CSV files and visualizes hourly vehicle frequency using a custom-built histogram implemented with **Tkinter** (no external libraries).

---

## 📌 Features

- 📅 User-validated date input with leap-year handling  
- 📊 Automatic processing of traffic CSV files  
- 📈 Interactive histogram showing vehicle frequency per hour  
- 🧮 Calculates:
  - Total vehicles  
  - Trucks, electric vehicles, two-wheelers  
  - Buses heading north  
  - Vehicles not turning  
  - Speeding vehicles  
  - Junction-specific statistics  
  - Rain hour count  
- 💾 Results saved automatically to `results.txt`  
- 🔁 Supports multiple CSV files in one session  

---

## 🗂 Project Structure

```
.
├── traffic_dataDDMMYYYY.csv
├── results.txt
├── traffic_analyser.py
└── README.md
```

---

## ▶ How to Run

Make sure Python is installed.

```bash
python traffic_analyser.py
```

---

## 🧾 Input File Format

CSV file name format:

```
traffic_dataDDMMYYYY.csv
```

Example:

```
traffic_data27112024.csv
```

Required columns:

- `timeOfDay`  
- `JunctionName`  
- `VehicleType`  
- `VehicleSpeed`  
- `JunctionSpeedLimit`  
- `travel_Direction_in`  
- `travel_Direction_out`  
- `elctricHybrid`  
- `Weather_Conditions`  

---

## 📊 Histogram View

When prompted:

```
Would you like to see a histogram of vehicle frequency per hour? (yes/no):
```

Type **yes** to display a graphical histogram for:

- Elm Avenue / Rabbit Road  
- Hanley Highway / Westway  

---

## 💡 Sample Output

```
Data file selected: traffic_data27112024.csv
Total vehicles recorded: 421
Total trucks recorded: 78
Total electric vehicles recorded: 43
Total two-wheeled vehicles recorded: 64
Total buses heading North from Elm Avenue/Rabbit Road: 11
Total vehicles not turning left or right: 53
Percentage of trucks: 19%
Total vehicles over speed limit: 29
Total vehicles through Elm Avenue/Rabbit Road: 211
Total vehicles through Hanley Highway/Westway: 210
Percentage of scooters at Elm Avenue/Rabbit Road: 14%
Highest number of vehicles in an hour at Hanley Highway/Westway: 37
Peak hour at Hanley Highway/Westway: 17:00 to 18:00
Hours of rain: 6
******************************
```

---

## 🛠 Technologies Used

- Python 3  
- Tkinter  
- CSV & Datetime modules  

---

## 🎯 Learning Outcomes

- CSV file handling  
- Input validation  
- Data aggregation & statistics  
- GUI programming with Tkinter  
- Modular Python development  
