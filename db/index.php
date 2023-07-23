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
        
        input[type=text] {
            width: 100%;
            padding: 12px 20px;
            margin: 8px 0;
            box-sizing: border-box;
        }
        
        input[type=button],
        input[type=submit],
        input[type=reset] {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 16px 32px;
            text-decoration: none;
            margin: 4px 2px;
            cursor: pointer;
            width: 100%;
        }
    </style>
</head>

<body>
    <center>
        <form action="get-data.php" method="post">
            <h1>Type Stock Code</h1>
            <input name="code" type="text" value='SSSTEEL,UNIQUEHRL,MICEMENT,ROBI,BEXIMCO' placeholder="Type code separated by comma.." />
            <input name="ok" type="submit" value="Submit" />
        </form>


    </center>
</body>

</html>