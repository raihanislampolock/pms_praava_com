import json
import psycopg2
import json
import canon_337
import hp_508_printer
import Brother
from datetime import datetime
import pytz


# Constants for database connection
DB_HOST = "20.198.153.150"
DB_PORT = 5432
DB_NAME = "pms"
DB_USER = "consult"
DB_PASSWORD = "consult1234"

dhaka_tz = pytz.timezone("Asia/Dhaka")

def insert_printer_details(printer_details):
    conn = None
    cursor = None
    try:
        # Set up database connection
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        # Create a cursor object
        cursor = conn.cursor()

        for location, details in printer_details.items():
            ip = details['ip']
            status = details['status']
            device_status = details['device_status']
            details_json = json.dumps(details['percentage'])
            created_at = datetime.now(dhaka_tz)

            cursor.execute(
                "INSERT INTO printer_details (location, ip, details, device_status, status, created_at) VALUES (%s, %s, %s, %s, %s, %s)",
                (location, ip, details_json, device_status, status, created_at)
            )

        # Commit changes to the database
        conn.commit()
    except Exception as e:
        print(f"Error inserting printer details: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def delete_old_printer_details():
    conn = None
    cursor = None

    try:
        # Set up database connection
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        # Delete printer details older than 7 days
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM printer_details WHERE created_at < NOW() - INTERVAL '7 days'"
        )

        # Commit changes and close the database connection
        conn.commit()
    except Exception as e:
        print(f"Error deleting old printer details: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# Get printer details
hp_508_details = hp_508_printer.printer_508_details()
canon_337_details = canon_337.get_cartridge_info()
brother_details = Brother.printer_brother_details()

# Insert printer details into the database
insert_printer_details(hp_508_details)
insert_printer_details(canon_337_details)
insert_printer_details(brother_details)


# Delete old printer details from the database
delete_old_printer_details()
