<?php
$output = exec('env/bin/python3 /Users/icesiv/work/db_stock_data/grab_top.py 2>&1', $output2);
print_r(error_get_last());
echo $output2;
echo $output;
?>