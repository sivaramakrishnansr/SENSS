<?php
function display_threshold($int_threshold) {
        $zeros = log($int_threshold) / log(10);
        if ($zeros >= 12) {
                return round($int_threshold / pow(10, 12),2)." TBps";
        } else if ($zeros >= 9) {
                return round($int_threshold / pow(10, 9),2)." GBps";
        } else if ($zeros >= 6) {
                return round($int_threshold / pow(10, 6),2)." MBps";
        } else if ($zeros >= 3) {
                return round($int_threshold / pow(10, 3),2)." KBps";
        } else {
                return $int_threshold." Bps";
        }
}
echo display_threshold(10000);
?>
