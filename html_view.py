import datetime
from email.mime import image
import background as background
import psycopg2
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

import pytz


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Set up database connection
        conn = psycopg2.connect(
            host="20.198.153.150",
            database="raihan_local",
            user="consult",
            password="consult1234"
        )
        cursor = conn.cursor()

        # Fetch data from database
        cursor.execute(
            "SELECT *, substring(location from '[0-9]+')::integer as \"location2\" FROM printer_details ORDER BY id DESC, \"location2\" ASC LIMIT 17")

        data = cursor.fetchall()
        # print(data)
        sorted_data = sorted(data, key=lambda x: x[-1])
        # Create HTML table
        table = "<table class='table'><thead><tr><th>ID</th><th>Location</th><th>IP</th><th>Details (%)</th><th>Date and Time</th><th>Status</th><th>Device Status</th></tr></thead><tbody>"
        for row in sorted_data:
            table += "<tr>"
            table += f"<td>{row[0]}</td>"
            table += f"<td style='font-weight:900;'>{row[1]}</td>"
            table += f"<td><a href='http://{row[2]}' target='_blank'>{row[2]}</a></td>"
            # table += f"<td>{row[3]}</td>"



            # Extracting data from the string
            details = row[3]
            details = details.replace("{", "").replace("}", "")
            details = details.replace('"', "").replace('"', "")
            details = details.replace(",", "<br>")
            # table += f"<td>{details}</td>"
            table += f"<td>"
            data = json.loads(row[3])
            for i in data:
                if isinstance(data[i], int) or isinstance(data[i], float):
                    value = str(data[i])
                else:
                    value = data[i].replace('%', '')
                if value:
                    if value.startswith("<"):
                        value = value[1:]  # Remove the leading "<" character
                    if value.isdigit() and int(value) <= 30:
                        table += f"<span style='color:red; font-weight:900;'>{i}: {value}</span><br>"
                    elif int(value) <= 50:
                        table += f"<span style='color:#17a2b8; font-weight:900;'>{i}: {value}</span><br>"
                    else:
                        table += f"<span style='color:black; font-weight:900;'>{i}: {value}</span><br>"
                else:
                     # handle the case where value is an empty string
                     table += f"<span style='color:black; font-weight:900;'>{i}: N/A</span><br>"

            table += f"</td>"

            local_time = row[5].astimezone(datetime.timezone(datetime.timedelta(hours=6, minutes=0)))
            local_time_str = local_time.strftime('%Y-%m-%d %H:%M:%S')
            # Set the timezone of the datetime object to UTC
            utc_time = pytz.utc.localize(row[5])

            # Convert the UTC datetime object to GMT+6
            local_time = utc_time.astimezone(pytz.timezone('Asia/Dhaka'))

            # Format the local datetime object as a string
            local_time_str = local_time.strftime('%Y-%b-%d <br> %H:%M:%S')

            table += f"<td>{local_time_str}</td>"
            if (row[8]=="online"):
                table += f"<td><span style='color:#17a2b8; font-weight:700; text-transform:capitalize;'>{row[8]}</span></td>"
            else:
                table += f"<td><span style='color:red; font-weight:700; text-transform:capitalize;'>{row[8]}</span></td>"

            table += f"<td style='font-weight:700; width: 200px;'>{row[9]}</td>"

            table += "</tr>"
        table += "</tbody></table>"

        # Close database connection
        cursor.close()
        conn.close()

        # Create HTML page with table and basic CSS style
        html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Printer Details</title>
                <meta http-equiv="refresh" content="10">
                <style>
                    body {{
                        font-family: Arial, Helvetica, sans-serif;
                        font-size: 16px;
                        margin: 0;
                        padding: 8px;

                    }}
                    
                    .table {{
                        border-collapse: collapse;
                        width: 100%;
                    }}
                    .table th, .table td {{
                        text-align: center;
                        padding: 8px;
                        border: 1px solid #3b3535;
                    }}
                    .table th {{
                        background-color: #8A2061;
                        color: #f5f7f5;
                    }}
                    .table tr:nth-child(even) {{
                        background-color: #c8c8c8;
                    }}
                    .table tr:hover {{
                        background-color: #9f9c97;
                    }}
                    .title {{
                       color: #8A2061;
                       text-align: center;
                       font-size: 30px;
                       font-weight: 900;
                    }}
                    @media only screen and (max-width: 600px) {{
                        .table {{
                            font-size: 12px;
                        }}
                        .table th, .table td {{
                            padding: 4px;
                        }}
                    }}

                </style>
            </head>
            <body>
            <h1 class="title">Praava Health Printer Details</h1>
                {table}
            </body>
            </html>
        """

        # Send response to client
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())


# Create HTTP server and start listening for incoming requests
httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
httpd.serve_forever()

