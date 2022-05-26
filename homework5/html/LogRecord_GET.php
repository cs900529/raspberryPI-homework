<?php
    $host = "localhost";
    $dbuser = "root";
    $dbpasswd = "123456";
    $DBNAME = "dht22_log";

    if(isset($_GET['TEMPC'])){
        $conn = mysqli_connect($host, $dbuser, $dbpasswd, $DBNAME);
        if(!$conn) {
            echo "Error: Unable to connect to MySQL." . PHP_EOL;
            echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
            echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;    
            die ("無法連接資料庫");
        }
        // 設定連線編碼
        mysqli_query($conn, "SET NAMES 'utf8'");

        $sql = sprintf("INSERT INTO log (`TEMPC`,`TEMPF`,`HUMD`,`logtime`) 
            VALUES ('%s','%s','%s',NOW());",
            $_GET['TEMPC'],$_GET['TEMPF'],$_GET['HUMD']
        );
        $ret = mysqli_query($conn, $sql);

        if(!$ret){
            echo "Error: Unable to connect to MySQL." . PHP_EOL;
            echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
            echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;    
            die("insert error");
        }else{
            echo "Records created successfully\n";
        }
        mysqli_close($conn);
    }else{
        die("Error");
    }
?>
