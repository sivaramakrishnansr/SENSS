<?php

function getIpRange($cidr)
{
    if (strpos($cidr, '/') == false) {
        $cidr .= '/32';
    }
    list($ip, $mask) = explode('/', $cidr);

    $maskBinStr = str_repeat("1", $mask) . str_repeat("0", 32 - $mask);      //net mask binary string
    $inverseMaskBinStr = str_repeat("0", $mask) . str_repeat("1", 32 - $mask); //inverse mask

    $ipLong = ip2long($ip);
    $ipMaskLong = bindec($maskBinStr);
    $inverseIpMaskLong = bindec($inverseMaskBinStr);
    $netWork = $ipLong & $ipMaskLong;

    $start = $netWork + 1;//ignore network ID(eg: 192.168.1.0)

    $end = ($netWork | $inverseIpMaskLong) - 1; //ignore brocast IP(eg: 192.168.1.255)
    return array('firstIP' => $start, 'lastIP' => $end);
}

function ip_in_range($ip, $range)
{
    if (strpos($range, '/') == false) {
        $range .= '/32';
    }
    // $range is in IP/CIDR format eg 127.0.0.1/24
    list($range, $netmask) = explode('/', $range, 2);
    $range_decimal = ip2long($range);
    $ip_decimal = ip2long($ip);
    $wildcard_decimal = pow(2, (32 - $netmask)) - 1;
    $netmask_decimal = ~$wildcard_decimal;
    return (($ip_decimal & $netmask_decimal) == ($range_decimal & $netmask_decimal));
}

function validate_ip_range($request_prefix, $client_prefix)
{
    $ip_range = getIpRange($request_prefix);
    return ip_in_range(long2ip($ip_range['firstIP']), $client_prefix) &&
        ip_in_range(long2ip($ip_range['lastIP']), $client_prefix);
}
