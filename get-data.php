<html>

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0,
            maximum-scale=1.0, user-scalable=0">
    <title>BD Stock</title>
    <style type="text/css">
    h1 {
        color: #111;
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 30px;
        font-weight: bold;
        letter-spacing: -1px;
        line-height: 1;
        text-align: center;
    }

    .styled-table {
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 0.9em;
        font-family: sans-serif;
        min-width: 400px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
    }

    .styled-table thead tr {
        background-color: #009879;
        color: #ffffff;
        text-align: left;
    }

    .styled-table th,
    .styled-table td {
        padding: 12px 15px;
    }

    .styled-table tbody tr {
        border-bottom: 1px solid #dddddd;
    }

    .styled-table tbody tr:nth-of-type(even) {
        background-color: #f3f3f3;
    }

    .styled-table tbody tr:last-of-type {
        border-bottom: 2px solid #009879;
    }

    .styled-table tbody tr.active-row {
        font-weight: bold;
        color: #009879;
    }
    </style>
</head>

<body>
    <center>
        <?php
        // $output = exec('env/bin/python3
        //         /Users/icesiv/work/db_stock_data/grab_top.py 2>&1', $output2);
        // print_r(error_get_last());

        // $str_data = $output;;
        // $data = json_decode($str_data, true);

        $json = file_get_contents('db/output/top_listing.json');

        // Decode the JSON file
        $json_data = json_decode($json, true);
        $json_data = $json_data[0];

        echo "<h1>" . $json_data['time'] . "</h1>";

        /*Initializing temp variable to design table dynamically*/
        $temp = "<table class='styled-table'>";

        /*Defining table Column headers */
        $temp .= "<tr>";
        $temp .= "<th>Code</th>";
        $temp .= "<th>LTP</th>";
        $temp .= "<th>High</th>";
        $temp .= "<th>Low</th>";
        $temp .= "</tr>";

        $all_stocks = $json_data["stocks"];
        //$all_stocks = $json_data;

        $picked_stocks = array();

        if (isset($_POST['ok'])) {
            $picked_code = explode(",", $_POST['code']);

            foreach ($picked_code as &$value) {
                $value = strtoupper($value);
                $value = trim($value);
            }
            unset($value);
        } else {
            $picked_code = array("SSSTEEL", "ROBI", "BEXIMCO");
        }


        foreach ($all_stocks as $key => $stock) {
            if (in_array($stock['code'], $picked_code)) {
                array_push($picked_stocks, $stock);
            }
        }

        /*Dynamically generating rows & columns*/
        for ($i = 0; $i < sizeof($picked_stocks); $i++) {
            $temp .= "<tr>";
            $temp .= "<td>" . $picked_stocks[$i]["code"] . "</td>";
            $temp .= "<td>" . $picked_stocks[$i]["ltp"] . "</td>";
            $temp .= "<td>" . $picked_stocks[$i]["high"] . "</td>";
            $temp .= "<td>" . $picked_stocks[$i]["low"] . "</td>";
            $temp .= "</tr>";
        }

        /*End tag of table*/
        $temp .= "</table>";

        /*Printing temp variable which holds table*/

        echo $temp;
        ?>
    </center>
</body>

</html>