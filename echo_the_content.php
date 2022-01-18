<?php
	header("Content-type: text/plain");
	
	//how to use:
	//this is a small helper php script to get the content of log files
	//and to monitor the downloads foldee to show whats happening on anime-loads-dl-manual.php
	
	//TO EDIT:
	$pathDownloadsFolder = '/volume1/Downloads';
	$pathManualOutputLog = '/volume1/docker-configs/anime-loads/manualOutput.log';
	$pathAniJson = '/volume1/docker-configs/anime-loads/ani.json';
	$pathAniJson = '/volume1/docker-configs/anime-loads/ani.json';
	$pathDownloadAndMonitoring = '/volume1/docker-configs/anime-loads/downloading_and_monitoring.txt';
	$pathNoReleasesFound = '/volume1/docker-configs/anime-loads/no_releases_found_log.txt';
	//EDIT END
	
	//
	// Converts Bashoutput to colored HTML
	//
	function convertBash($code) {
		$dictionary = array(
			'[30m' => '<br><span style="color:black">',
			'[31m' => '<br><span style="color:red">', 
			'[32m' => '<br><span style="color:green">',   
			'[33m' => '<br><span style="color:orange">',
			'[34m' => '<br><span style="color:blue">',
			'[35m' => '<br><span style="color:purple">',
			'[36m' => '<br><span style="color:cyan">',
			'[37m' => '<br><span style="color:white">',
			'[m'   => '</span><br>',
			'[0m'   => '</span><br>'
		);
		$htmlString = str_replace(array_keys($dictionary), $dictionary, $code);
		//$htmlString = str_replace('\n', '<br>', $htmlString);
		return $htmlString;
	}



	if ($_GET['file'] == 1) {
		echo convertBash(file_get_contents($pathManualOutputLog));
	} else if ($_GET['file'] == 2) {
		$data = explode("\n",explode('"settings":', file_get_contents( $pathAniJson ))[0]);
		foreach(array_reverse($data) as $value) { 
			echo $value."\n";
		}
		//echo file_get_contents('/volume1/docker/anime-loads/ani.json');
	} else if ($_GET['file'] == 3) {
		echo file_get_contents($pathDownloadAndMonitoring);
	} else if ($_GET['file'] == 4) {
		echo file_get_contents($pathNoReleasesFound);
	} else if ($_GET['file'] == 5) {
		$output = shell_exec("find " . $pathDownloadsFolder . " -path '*german*tv*' -printf '%s -- %p\n' -o -path '*german*movie*' -printf '%s -- %p\n' -o -path '*japanese*tv*' -printf '%s -- %p\n' -o -path '*japanese*movie*' -printf '%s -- %p\n' | grep -v -E 'completed|series_complete|intermediate|movies_complete|tmp'");// | grep -oP '[^/]*$'
		$output = preg_replace('/[^\d\s-].*\//', '', $output);
		$output = preg_replace('/[^\d\s-].*$/', '', $output);
		$output = preg_replace('/32 -- /', '<br />', $output);
		$output = nl2br($output);
		echo $output;
	}
	
?>
