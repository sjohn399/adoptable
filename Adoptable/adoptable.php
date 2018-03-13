<?php 
/* 
Author: Samuel Johnson
Date: 3/2/2018

*/
//Extract variables

extract($_POST);

$url = 'http://localhost:9000/api';
$curl = curl_init($url);

$file = fopen("trainingCases.csv", "r");

$importArray = array();

while(($data = fgetcsv($file)) != False)
{
	$importArray[] = $data;
}

fclose($file);

$importArray = $importArray[0];

array_shift($importArray);

$importArray = array_flip($importArray);

foreach ($importArray as $key => &$value)
{
	if ($key == $size){
		$value = 1;
	}
	else if ($key == $sex) {
		$value = 1;
	}
	else if ($key == $mix) {
		$value = 1;
	}
	else if ($key == $age) {
		$value = 1;
	}
	else if ($key == $breed1) {
		$value = 1;
	}
	else if ($key == $breed2) {
		$value = 1;
	}
	else
	{
		$value = 0;
	}
}

unset($value);

$jsonData = json_encode($importArray);

curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_POST, true);
curl_setopt($curl, CURLOPT_POSTFIELDS, $jsonData);

$response = curl_exec($curl);

if ($response == false)
{
	$info = curl_getinfo($curl);
	curl_close($curl);
	die('error occured during curl exec. Additional info: ' . var_export($info));
}

curl_close($curl);

$decoded = json_decode($response, true);
$numDays = $decoded['predictions'][0];

$years = intdiv($numDays, 365);
$months = intdiv(($numDays - $years * 365), 30);
$days = $numDays - $years * 365 - $months * 30;

?>

<html>
	<head>
		<link rel="stylesheet" type = "text/css" href="adoptable.css">
		<style>
			body {
				background-image: url("pupper2.jpg");
			}
		</style>
	</head>
	<body>
		<h1><span class = "purple">Time To </span><span class = "outline">Adoption</span></h1>
		<div id = "container">
			<div id = "report">
				<ul>
					<li>Years: <div class = "output"><?php print $years ?></div></li>
					<li>Months: <div class = "output"><?php print $months ?></div></li>
					<li>Days: <div class = "output"><?php print $days ?></div></li>
				</ul>
			</div>
		</div>
	</body>
</html>