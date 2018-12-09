<?php

function get_domain($domain)
{
	$original = $domain = strtolower($domain);
    	return $original;
    	if (filter_var($domain, FILTER_VALIDATE_IP)) { return $domain; }

    	$arr = array_slice(array_filter(explode('.', $domain, 4), function($value){
        	return $value !== 'www';
    	}), 0); //rebuild array indexes

    	if (count($arr) > 2)
    	{
        	$count = count($arr);
        	$_sub = explode('.', $count === 4 ? $arr[3] : $arr[2]);

        	if (count($_sub) === 2) // two level TLD
        	{
            		$removed = array_shift($arr);
            		if ($count === 4) // got a subdomain acting as a domain
            		{
                		$removed = array_shift($arr);
            		}
        	}
        	elseif (count($_sub) === 1) // one level TLD
        	{
            		$removed = array_shift($arr); //remove the subdomain

            		if (strlen($_sub[0]) === 2 && $count === 3) // TLD domain must be 2 letters
            		{
                		array_unshift($arr, $removed);
            		}
            		else
            		{
                		// non country TLD according to IANA
                		$tlds = array(
                    			'aero',
                    			'arpa',
                    			'asia',
                    			'biz',
                    			'cat',
                    			'com',
                    			'coop',
                    			'edu',
                    			'gov',
                    			'info',
                    			'jobs',
                    			'mil',
                    			'mobi',
                    			'museum',
                    			'name',
                    			'net',
                    			'org',
                    			'post',
                    			'pro',
                    			'tel',
                    			'travel',
                		);

                		if (count($arr) > 2 && in_array($_sub[0], $tlds) !== false) //special TLD don't have a country
                		{
                    			array_shift($arr);
                		}
            		}
        	}
        	else // more than 3 levels, something is wrong
        	{
            		for ($i = count($_sub); $i > 1; $i--)
            		{
                		$removed = array_shift($arr);
            		}
        	}
    	}
    	elseif (count($arr) === 2)
    	{
       		$arr0 = array_shift($arr);

        	if (strpos(join('.', $arr), '.') === false
            		&& in_array($arr[0], array('localhost','test','invalid')) === false) // not a reserved domain
        	{
            	// seems invalid domain, restore it
            		array_unshift($arr, $arr0);
        	}
    	}

    	return join('.', $arr);
}

function client_auth($headers) {
    	if (!isset($headers['X-Client-Cert'])) {
        	http_response_code(400);
		return 10;
        	return false;
    	}
    	$client_cert = $headers['X-Client-Cert'];
    	$client_cert = base64_decode($client_cert);

    	set_include_path(get_include_path() . PATH_SEPARATOR . 'phpseclib');
    	include('File/X509.php');

    	$x509 = new File_X509();
    	$pemcacert = file_get_contents('/var/www/html/SENSS/UI_client_server/Server/cert/rootcert.pem');
    	$x509->loadCA($pemcacert);
    	$x509->loadX509($client_cert);
    	if (!$x509->validateSignature()) {
        	http_response_code(400);
		return 0;
        	return false;
    	}
    	$cert_content = openssl_x509_parse($client_cert);
    	return array(
        	'client_prefix' => $cert_content['extensions']['nsComment'],
        	'as_domain' => get_domain($cert_content['subject']['CN'])
    	);
}
