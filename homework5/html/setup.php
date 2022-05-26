<?php
    // 這個檔案拿來建立資料庫環境
    $host = "localhost";
    $dbuser = "root";
    $dbpasswd = "123456";
    
    $create_db_sql = "CREATE DATABASE IF NOT EXISTS `dht22_log`;";
    $create_table_sql = "CREATE TABLE IF NOT EXISTS `dht22_log`.`log` ( `index_id` INT NOT NULL AUTO_INCREMENT , `TEMPC` VARCHAR(20) NOT NULL ,  `TEMPF` VARCHAR(20) NOT NULL , `HUMD` VARCHAR(20) NOT NULL , `logtime` TIMESTAMP NOT NULL , PRIMARY KEY (`index_id`)) ENGINE = InnoDB;";

    $conn = mysqli_connect($host, $dbuser, $dbpasswd);
    
    if(!$conn){
        echo "Error: Unable to connect to MySQL." . PHP_EOL;
        echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
        echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;
        die("無法連線至資料庫");
    }
    $ret = mysqli_query($conn, $create_db_sql);
    if(!$ret){
        echo "Error: Unable to connect to MySQL." . PHP_EOL;
        echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
        echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;
        die("建立db失敗");
    }
    // 設定連線編碼
    mysqli_query($conn, "SET NAMES 'utf8'");

    // 建立table
    $ret = mysqli_query($conn, $create_table_sql);

    if(!$ret){
        echo "Error: Unable to connect to MySQL." . PHP_EOL;
        echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
        echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;
        die("建立table失敗");
    }
    echo "All OK";
    mysqli_close($conn);
?>
