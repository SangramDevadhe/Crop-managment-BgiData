import mysql.connector
import random
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker for generating random data
fake = Faker()

# MySQL Database Connection Details
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Root@1234",
    "database": "student"
}

# Connect to MySQL
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Create crops table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS crops (
    id INT AUTO_INCREMENT PRIMARY KEY,
    crop_name VARCHAR(255) NOT NULL,
    planting_date DATE,
    harvest_date DATE,
    growth_stage VARCHAR(255),
    pest_control_measures TEXT,
    yield_prediction INT
)
""")
conn.commit()

# List of sample crop names
crop_names = ["Wheat", "Rice", "Corn", "Soybean", "Barley", "Sugarcane", "Cotton", "Potato", "Tomato", "Lettuce"]

# List of possible growth stages
growth_stages = ["Seedling", "Vegetative", "Flowering", "Fruiting", "Maturity"]

# List of sample pest control measures
pest_control_measures_list = [
    "Use of organic pesticides",
    "Crop rotation",
    "Neem oil application",
    "Biological pest control",
    "Chemical pesticides",
    "Regular field monitoring",
]

# Function to generate random data for crops
def generate_data():
    crop_name = random.choice(crop_names)
    planting_date = fake.date_between(start_date="-2y", end_date="today")  # Planting in last 2 years
    harvest_date = planting_date + timedelta(days=random.randint(60, 180))  # Harvest after 2-6 months
    growth_stage = random.choice(growth_stages)
    pest_control = random.choice(pest_control_measures_list)
    yield_prediction = random.randint(500, 5000)  # Yield in kg
    
    return (crop_name, planting_date, harvest_date, growth_stage, pest_control, yield_prediction)

# Batch insert records in chunks
batch_size = 1  # Insert 10,000 at a time for efficiency
total_records = 1000000

for i in range(0, total_records, batch_size):
    data_batch = [generate_data() for _ in range(batch_size)]
    
    # Execute batch insert
    cursor.executemany("""
        INSERT INTO crops (crop_name, planting_date, harvest_date, growth_stage, pest_control_measures, yield_prediction)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, data_batch)
    conn.commit()
    
    print(f"{i + batch_size} records inserted...")

print("✅ Data insertion completed successfully!")

# Close the database connection
cursor.close()
conn.close()
