#Author: M. M. Kolambage
#Date: 27/11/2024
#Student ID: w2120063

import csv  #for reading from and writing to CSV files
from datetime import datetime  #This allows you to work with date and time objects
import tkinter as tk  # Add this import for the histogram

# Add the HistogramApp class here

#Task D
class HistogramApp:
    def __init__(self, filename):
        self.filename = filename
        self.traffic_data = self.load_csv_data()
        date_str = filename.split('traffic_data')[1].split('.csv')[0]
        self.date = datetime.strptime(date_str, '%d%m%Y').strftime('%d/%m/%Y')
        
        self.root = tk.Tk()
        self.root.title("Histogram")
        
        # Window dimensions - make it wider and shorter for the desired aspect ratio
        self.WIDTH = 1500
        self.HEIGHT = 500
        
        # Margins
        self.MARGIN_LEFT = 50
        self.MARGIN_RIGHT = 50
        self.MARGIN_TOP = 80
        self.MARGIN_BOTTOM = 80
        
        # Bar settings
        self.BAR_WIDTH = 20
        self.BAR_GAP = 2
        
        # Create canvas with white background
        self.canvas = tk.Canvas(
            self.root, 
            width=self.WIDTH, 
            height=self.HEIGHT, 
            bg='white'
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Center window on screen
        x = (self.root.winfo_screenwidth() - self.WIDTH) // 2
        y = (self.root.winfo_screenheight() - self.HEIGHT) // 2
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")

    def load_csv_data(self):
        traffic_data = {
            'Elm Avenue/Rabbit Road': {hour: 0 for hour in range(24)},
            'Hanley Highway/Westway': {hour: 0 for hour in range(24)}
        }
        
        try:
            with open(self.filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    hour = int(datetime.strptime(row['timeOfDay'], '%H:%M:%S').hour)
                    junction = row['JunctionName']
                    if junction in traffic_data:
                        traffic_data[junction][hour] += 1
            return traffic_data
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    def setup_window(self):
        self.max_value = 0
        for junction in self.traffic_data.values():
            for count in junction.values():
                self.max_value = max(self.max_value, count)

        self.plot_width = self.WIDTH - (self.MARGIN_LEFT + self.MARGIN_RIGHT)
        self.plot_height = self.HEIGHT - (self.MARGIN_TOP + self.MARGIN_BOTTOM)

    def add_legend(self):
        # Colors matching the image
        colors = ['#0072B2', '#E69F00']  # Blue and Orange
        names = list(self.traffic_data.keys())
        
        # Position legend items horizontally at the top
        y = 30
        x_start = self.MARGIN_LEFT
        vertical_spacing = 30
        
        for i, (color, name) in enumerate(zip(colors, names)):
            # Draw colored rectangle
            self.canvas.create_rectangle(
                x_start, y - 8,
                x_start + 16, y + 8,
                fill=color,
                outline='gray'
            )
            
            # Add junction name
            self.canvas.create_text(
                x_start + 25, y,
                text=name,
                anchor='w',
                font=('Arial', 10, 'bold')
            )
            
            y += vertical_spacing  # Space between legend items

    def draw_axes(self):
        # Draw subtle grid lines
        y_step = self.plot_height / 5
        for i in range(1, 6):
            y = self.HEIGHT - self.MARGIN_BOTTOM - (i * y_step)
            self.canvas.create_line(
                self.MARGIN_LEFT, y,
                self.WIDTH - self.MARGIN_RIGHT, y,
                fill='#EEEEEE'
            )

        # X-axis line
        self.canvas.create_line(
            self.MARGIN_LEFT, self.HEIGHT - self.MARGIN_BOTTOM,
            self.WIDTH - self.MARGIN_RIGHT, self.HEIGHT - self.MARGIN_BOTTOM,
            width=2, fill = "black"
        )
        
        text_x = (self.MARGIN_LEFT + (self.WIDTH - self.MARGIN_BOTTOM)) // 2
        text_y = self.HEIGHT - self.MARGIN_BOTTOM + 40
        self.canvas.create_text(
            text_x, text_y, text="Hours(00:00 to 23:00)", font=("Arial", 12, 'bold'), fill="blue"
        )# Naming of x axis
        
        text_x = self.MARGIN_LEFT - 20  # Slightly to the left of the Y-axis
        text_y = (self.MARGIN_TOP + self.HEIGHT - self.MARGIN_BOTTOM) // 2  # Center of Y-axis
        self.canvas.create_text(
            text_x, text_y, text="Vehicle Frequency", font=("Arial", 12, 'bold'), fill="blue", angle=90
        )# Naming of y axis

        
        

        # Hour labels
        for hour in range(24):
            x1 = self.MARGIN_LEFT + hour * ((self.plot_width) / 23)
            x2 = self.MARGIN_LEFT + (hour + 0.75) * ((self.plot_width) / 23)
            x = (x1 + x2) / 2
            formatted_hour = f"{hour:02}"
            self.canvas.create_text(
                x, self.HEIGHT - self.MARGIN_BOTTOM + 20,
                text=formatted_hour,
                font=('Arial', 8, 'bold'),
                
            )

    def draw_histogram(self):
        colors = ['#0072B2', '#E69F00']  # Blue and Orange
        hour_spacing = self.plot_width / 23
        
        for junction_idx, (junction_name, junction_data) in enumerate(self.traffic_data.items()):
            for hour, count in junction_data.items():
                # Calculate bar positions
                x1 = (self.MARGIN_LEFT + hour * hour_spacing + 
                      (junction_idx * (self.BAR_WIDTH + self.BAR_GAP)))
                y1 = self.HEIGHT - self.MARGIN_BOTTOM
                x2 = x1 + self.BAR_WIDTH
                y2 = y1 - (count / self.max_value * self.plot_height)
                
                # Draw bar
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=colors[junction_idx],
                    outline='grey'
                )
                
                # Add value on top
                if count > 0:
                    self.canvas.create_text(
                        (x1 + x2) / 2,
                        y2 - 5,
                        text=str(count),
                        font=('Arial', 8, 'bold'),
                        angle= 0
                    )

    def add_title(self):
        title = f"Histogram of Vehicle Frequency per Hour ({self.date})"
        self.canvas.create_text(
            self.WIDTH / 2,
            15,
            text=title,
            font=('Arial', 12, 'bold')
        )

    def run(self):
        if self.traffic_data is None:
            return
        
        self.setup_window()
        self.add_title()
        self.add_legend()
        self.draw_axes()
        self.draw_histogram()
        self.root.mainloop()


#Task A
def validate_date_input():
    
    """Validate and format the date input."""

    def is_leap_year(year):
        """Check if a given year is a leap year."""
        return (year % 4 == 0) and (year % 100 != 0 or year % 400 == 0)

    def get_the_year():
        while True:
            try:
                year = int(input("Enter the required year (YYYY): "))
                if 2000 <= year <= 2024:
                    return year
                print("Invalid input. Please enter a year between 2000 and 2024.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def get_the_month():
        while True:
            try:
                month = int(input("Enter the required month (MM): "))
                if 1 <= month <= 12:
                    return month
                print("Invalid input. Please enter a number between 1 and 12.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def get_the_day(year, month):
        while True:
            try:
                day = int(input("Enter the required day (DD): "))
                
                # Handle months with specific day counts
                if month in {1, 3, 5, 7, 8, 10, 12} and 1 <= day <= 31:  # 31-day months
                    return day
                elif month in {4, 6, 9, 11} and 1 <= day <= 30:  # 30-day months
                    return day
                elif month == 2:  # February
                    if is_leap_year(year):
                        if 1 <= day <= 29:  # Leap year February
                            return day
                        else:
                            print("Invalid input. February has 29 days in a leap year.")
                    else:
                        if 1 <= day <= 28:  # Non-leap year February
                            return day
                        else:
                            print("Invalid input. February has only 28 days in a non-leap year.")
                else:
                    print(f"Invalid input. The month {month} does not have {day} days.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    # Main date input flow
    year = get_the_year()
    month = get_the_month()
    day = get_the_day(year, month)

    
   
    return f"{day:02d}{month:02d}{year}" #as it is in DDMMYYYY


#Task B
def process_csv_data(date, file_path, results):
    try:
        
        with open(file_path, newline='') as file:
            reader = csv.DictReader(file)

            # Initialize counters and storage
            total_vehicles = 0
            total_trucks = 0
            total_electric_vehicles = 0
            total_two_wheeled = 0
            total_busses_north = 0
            total_no_turn = 0
            speeding_vehicles = 0
            vehicles_elm = 0
            vehicles_hanley = 0
            scooters_elm = 0
            hourly_hanley = {}
            hours_of_rain = 0

            # Process each row
            for row in reader:
                total_vehicles += 1

                # Vehicle type counts
                if row['VehicleType'] == 'Truck':
                    total_trucks += 1
                if row['elctricHybrid'].lower() == 'true':
                    total_electric_vehicles += 1
                if row['VehicleType'] in ['Bike', 'Scooter']:
                    total_two_wheeled += 1
                if row['VehicleType'] == 'Buss' and row['travel_Direction_out'] == 'N':
                    total_busses_north += 1

                # No turn
                if row['travel_Direction_in'] == row['travel_Direction_out']:
                    total_no_turn += 1

                # Speeding vehicles
                if int(row['VehicleSpeed']) > int(row['JunctionSpeedLimit']):
                    speeding_vehicles += 1

                # Junction-specific counts
                if row['JunctionName'] == 'Elm Avenue/Rabbit Road':
                    vehicles_elm += 1
                    if row['VehicleType'] == 'Scooter':
                        scooters_elm += 1
                if row['JunctionName'] == 'Hanley Highway/Westway':
                    vehicles_hanley += 1
                    hour = datetime.strptime(row['timeOfDay'], '%H:%M:%S').hour
                    if hour not in hourly_hanley:
                        hourly_hanley[hour] = 0
                    hourly_hanley[hour] += 1

                # Rain condition
                if 'Rain' in row['Weather_Conditions']:
                    hours_of_rain += 1

            # Calculating the results
            percentage_trucks = round((total_trucks / total_vehicles) * 100)
            percentage_scooters_elm = round((scooters_elm / vehicles_elm) * 100) if vehicles_elm else 0
            highest_vehicles_hanley = max(hourly_hanley.values(), default=0)
            peak_hour_hanley = max(hourly_hanley, key=hourly_hanley.get, default=None)

            # Collect results in a list
            result_lines = [
                f"Data file selected: traffic_data{date}.csv",
                f"Total vehicles recorded: {total_vehicles}",
                f"Total trucks recorded: {total_trucks}",
                f"Total electric vehicles recorded: {total_electric_vehicles}",
                f"Total two-wheeled vehicles recorded: {total_two_wheeled}",
                f"Total buses heading North from Elm Avenue/Rabbit Road: {total_busses_north}",
                f"Total vehicles not turning left or right: {total_no_turn}",
                f"Percentage of trucks: {percentage_trucks}%",
                f"Total vehicles over speed limit: {speeding_vehicles}",
                f"Total vehicles through Elm Avenue/Rabbit Road: {vehicles_elm}",
                f"Total vehicles through Hanley Highway/Westway: {vehicles_hanley}",
                f"Percentage of scooters at Elm Avenue/Rabbit Road: {percentage_scooters_elm}%",
                f"Highest number of vehicles in an hour at Hanley Highway/Westway: {highest_vehicles_hanley}",
            ]

            if peak_hour_hanley is not None:
                result_lines.append(f"Peak hour at Hanley Highway/Westway: {peak_hour_hanley}:00 to {peak_hour_hanley + 1}:00")
            else:
                result_lines.append("No data for peak hour at Hanley Highway/Westway.")

            result_lines.append(f"Hours of rain: {hours_of_rain}")
            result_lines.append("*" * 30)

            # Add the results to the main list
            results.extend(result_lines)

            # Print the results in the shell
            for line in result_lines:
                print(line)

        

        
        while True:
            show_histogram = input("Would you like to see a histogram of vehicle frequency per hour? (yes/no): ").strip().lower()
            if show_histogram == 'yes':
                app = HistogramApp(file_path)
                app.run()
                break
            elif show_histogram == 'no':
                break
            else:
                print("Please enter 'yes' or 'no'.")

    except FileNotFoundError:
        print(f"Error: The file 'traffic_data{date}.csv' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

#Task C
def save_results_to_file(results):
    
    """Save the results list to a text file."""
    try:
        with open("results.txt", "w") as file:
            for line in results:
                file.write(line + "\n")
        print("Results saved to 'results.txt'.")
    except Exception as e:
        print(f"An error occurred while saving results: {e}")


def main():
    
    """Main program function."""
    results = []
    while True:
        date = validate_date_input()
        file_path = f"traffic_data{date}.csv"
        
        # Attempt to process the CSV data
        try:
            process_csv_data(date, file_path, results)
        except FileNotFoundError:
            print(f"File '{file_path}' not found. Please try again.")
            continue  # Skip to the next iteration of the loop

        while True:
            retry = input("Would you like to try another date? (yes/no): ").strip().lower()
            if retry == 'yes':
                break  # Continue the outer loop
            elif retry == 'no':
                if results:  # Only save if there is data in the results
                    save_results_to_file(results)
                    print("Results have been saved.")
                else:
                    print("No data to save. Exiting program.")
                print("Goodbye!")
                return  # Exit the function
            else:
                print("Please enter 'yes' or 'no'. Thank you.")
#Task E
class MultiCSVProcessor:
    def __init__(self):
        self.results = []

    def process_files(self):
        while True:
            date = validate_date_input()
            file_path = f"traffic_data{date}.csv"
            
            try:
                # Only process data first
                process_csv_data(date, file_path, self.results)
                
                # Handle retry input
                while True:
                    retry = input("Would you like to try another date? (yes/no): ").strip().lower()
                    if retry == 'yes':
                        break
                    elif retry == 'no':
                        if self.results:
                            save_results_to_file(self.results)
                            print("Results have been saved.")
                        else:
                            print("No data to save. Exiting program.")
                        print("Goodbye!")
                        return
                    else:
                        print("Please enter 'yes' or 'no'. Thank you.")
                        
            except FileNotFoundError:
                print(f"File '{file_path}' not found. Please try again.")

def enhanced_main():
    processor = MultiCSVProcessor()
    processor.process_files()

if __name__ == "__main__":
    enhanced_main()    

