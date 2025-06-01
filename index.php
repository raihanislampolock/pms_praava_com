<?php
// Set default timezone
date_default_timezone_set('Asia/Dhaka');

// Function to convert UTC timestamp to Asia/Dhaka
function getLocalTime($utcTime) {
    $utcDateTime = new DateTime($utcTime, new DateTimeZone('UTC'));
    $localTimeZone = new DateTimeZone('Asia/Dhaka');
    $utcDateTime->setTimezone($localTimeZone);
    return $utcDateTime->format('Y-m-d <br> H:i:s');
}

// Database credentials
$host = "20.198.153.150";
$database = "pms";
$user = "consult";
$password = "consult1234";

try {
    // Connect to PostgreSQL
    $conn = new PDO("pgsql:host=$host;dbname=$database", $user, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Fetch printer details with parsed location number
    $query = "SELECT *, substring(location from '[0-9]+')::integer as \"location2\" FROM printer_details ORDER BY id DESC, \"location2\" ASC LIMIT 17";
    $stmt = $conn->prepare($query);
    $stmt->execute();
    $data = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Sort the data manually by location number
    usort($data, function($a, $b) {
        return $a['location2'] - $b['location2'];
    });

    // Start building HTML table
    $table = "<table class='table'><thead><tr><th>ID</th><th>Location</th><th>IP</th><th>Details (%)</th><th>Date and Time</th><th>Status</th><th>Device Status</th></tr></thead><tbody>";

    foreach ($data as $row) {
        $table .= "<tr>";
        $table .= "<td>{$row['id']}</td>";
        $table .= "<td style='font-weight:900;'>{$row['location']}</td>";
        $table .= "<td><a href='http://{$row['ip']}' target='_blank'>{$row['ip']}</a></td>";

        // Parse JSON details
        $details = json_decode($row['details'], true);
        $table .= "<td>";
        foreach ($details as $key => $value) {
            if (is_numeric($value)) {
                $value = strval($value);
            } else {
                $value = str_replace('%', '', $value);
            }

            if (!empty($value)) {
                if (strpos($value, '<') === 0) {
                    $value = substr($value, 1);
                }

                if (is_numeric($value) && intval($value) <= 30) {
                    $table .= "<span style='color:red; font-weight:900;'>{$key}: {$value}</span><br>";
                } elseif (intval($value) <= 50) {
                    $table .= "<span style='color:#17a2b8; font-weight:900;'>{$key}: {$value}</span><br>";
                } else {
                    $table .= "<span style='color:black; font-weight:900;'>{$key}: {$value}</span><br>";
                }
            } else {
                $table .= "<span style='color:black; font-weight:900;'>{$key}: N/A</span><br>";
            }
        }
        $table .= "</td>";

        // Convert UTC to local time
        $localTimeStr = getLocalTime($row['created_at']);
        $table .= "<td>{$localTimeStr}</td>";

        // Online/offline status
        if ($row['status'] == "online") {
            $table .= "<td><span style='color:#17a2b8; font-weight:700; text-transform:capitalize;'>{$row['status']}</span></td>";
        } else {
            $table .= "<td><span style='color:red; font-weight:700; text-transform:capitalize;'>{$row['status']}</span></td>";
        }

        $table .= "<td style='font-weight:700; width: 200px;'>{$row['device_status']}</td>";
        $table .= "</tr>";
    }

    $table .= "</tbody></table>";

    // Final HTML output
    $html = <<<HTML
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Printer Details</title>
    <meta http-equiv="refresh" content="10">
    <style>
        body {
            font-family: Arial, Helvetica, sans-serif;
            font-size: 16px;
            margin: 0;
            padding: 8px;
        }

        .table {
            border-collapse: collapse;
            width: 100%;
        }

        .table th, .table td {
            text-align: center;
            padding: 8px;
            border: 1px solid #3b3535;
        }

        .table th {
            background-color: #8A2061;
            color: #f5f7f5;
        }

        .table tr:nth-child(even) {
            background-color: #c8c8c8;
        }

        .table tr:hover {
            background-color: #9f9c97;
        }

        .title {
            color: #8A2061;
            text-align: center;
            font-size: 30px;
            font-weight: 900;
        }

        @media only screen and (max-width: 600px) {
            .table {
                font-size: 12px;
            }

            .table th, .table td {
                padding: 4px;
            }
        }
    </style>
</head>
<body>
<h1 class="title">Praava Health Printer Details</h1>
{$table}
</body>
</html>
HTML;

    // Send final response
    http_response_code(200);
    header('Content-type: text/html');
    echo $html;

    // Close connection
    $conn = null;

} catch(PDOException $e) {
    echo "Error: " . $e->getMessage();
}
?>
