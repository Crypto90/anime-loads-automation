<?php
set_time_limit(0);
session_start();


//TO EDIT:
$WEB_USER = "admin";
$WEB_PASSWORD = "A_GREAT_PASSWORD";
$download_anime_python_dir = '/volume1/docker-config/anime-loads';
$pathManualOutputLog = '/volume1/docker-configs/anime-loads/manualOutput.log';
$pathAniJson = '/volume1/docker-configs/anime-loads/ani.json';
$pathDownloadAndMonitoring = '/volume1/docker-configs/anime-loads/downloading_and_monitoring.txt';
$pathNoReleasesFound = '/volume1/docker-configs/anime-loads/no_releases_found_log.txt';
//EDIT END


if ($_GET['action'] == "logout") {
	session_destroy();
	header("Refresh:0; url=anime-loads-dl-manual.php");
	die();
}

?>
<html>
<head>
	<!-- CSS only -->
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
	<!-- JavaScript Bundle with Popper -->
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
	<script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
	<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.min.js" integrity="sha256-VazP97ZCwtekAsvgPBSUwPFKdrwD3unUfSGVYrahUqU=" crossorigin="anonymous"></script>

	<style>
		* {
			color: #dddddd;
		}
		body {
			background-color: #000000;
			text-align: center;
			font-family: Arial, sans-serif;
		}
		input {
			color: #000000;	
			padding: 10px;
    		width: 100%;
    		margin-bottom: 20px;
		}
		a {
    		width: 248px;
    		display: inline-block;
    		text-decoration: none;
    		color: orange;
		}
		hr {
    		width: 300px;
    		height: 1px;
	        background-color: #ccc;
	        border: none;
		}
		
		.form-select {
    		margin-bottom: 20px;
		}
		
		pre, #manualOutput {
    		text-align: left;
    		border: 2px solid grey;
    		width: 80%;
    		margin: 0 auto;
    		max-height: 400px;
    		overflow: auto;
    		padding: 5px;
		}
		
		#processRunning {
			width: 800px;
			margin: 0 auto;
			margin-bottom: 30px;
		}
		.form-control:valid, .form-select:valid {
		  background-color:  #181A1B!important;
		  border-color: #333333;
		  color: #dddddd;
		}
		
	</style>
	<script>
		var lastDataPrinted = '';
		$("document").ready(function(){
		    setInterval(function(){
		    	$.get('/echo_the_content.php?file=1', function(data) {
					if (lastDataPrinted != data) {
						lastDataPrinted = data;
						
						var data = data.replace('[0m', '').replace('[33m', '');
						$("#manualOutput").html(data);
		        		$('#manualOutput').scrollTop($('#manualOutput')[0].scrollHeight);
		        		$('#manualOutput')
						  .animate({borderColor:'green'}, 400, 'linear')
						  .delay(200)
						  .animate({borderColor:'#808080'}, 400, 'linear');
		        		
		        		if (data.indexOf('Exit') != -1) {
		        			//refresh the other log files too
		        			setTimeout(
							  function() 
							  {
							    $.get('/echo_the_content.php?file=2', function(data2) {
									$("#anijson").html(data2);
									$('#anijson')
									  .animate({borderColor:'green'}, 400, 'linear')
									  .delay(200)
									  .animate({borderColor:'#808080'}, 400, 'linear');
			        			});
			        			$.get('/echo_the_content.php?file=3', function(data2) {
									$("#log1").html(data2);
						        	$('#log1').scrollTop($('#log1')[0].scrollHeight);
						        	$('#log1')
									  .animate({borderColor:'green'}, 400, 'linear')
									  .delay(200)
									  .animate({borderColor:'#808080'}, 400, 'linear');
			        			});
			        			$.get('/echo_the_content.php?file=4', function(data2) {
									$("#log2").html(data2);
						        	$('#log2').scrollTop($('#log2')[0].scrollHeight);
						        	$('#log2')
									  .animate({borderColor:'green'}, 400, 'linear')
									  .delay(200)
									  .animate({borderColor:'#808080'}, 400, 'linear');
			        			});
							  }, 8000);
		        			
		        		}
				   }
				});
		    },500);
		    
		    
		    
		    $.get('/echo_the_content.php?file=5', function(data) {
				$("#downloaded-files-data").html(data);
			});
		    setInterval(function(){
		    	$.get('/echo_the_content.php?file=5', function(data) {
					$("#downloaded-files-data").html(data);
				});
		    }, 3000);
		    
		    
		    
		    $('#manualOutput').scrollTop($('#manualOutput')[0].scrollHeight);
		    $('#log1').scrollTop($('#log1')[0].scrollHeight);
		    $('#log2').scrollTop($('#log2')[0].scrollHeight);
		    
		    
		    
		});
	</script>
</head>
<body>
<?php





$user = $_POST['user'];
$pass = $_POST['pass'];

$userGET = $_GET['user'];
$passGET = $_GET['pass'];

if(($user == $WEB_USER && $pass == $WEB_PASSWORD) || ($userGET == $WEB_USER && $passGET == $WEB_PASSWORD) || ($_SESSION['user'] == $WEB_USER && $_SESSION['pass'] == $WEB_PASSWORD))
{
    $_SESSION['user'] = $WEB_USER;
    $_SESSION['pass'] = $WEB_PASSWORD;
    
    
	
    
    if (!file_exists($pathManualOutputLog)) {
	    touch($pathManualOutputLog);
	}
	
    
    ?>
    
    
    <br>
    <div>
	    <a style="display: inline-block;" class="btn btn-danger" href="anime-loads-dl-manual.php?action=logout">Logout</a>
    </div>

    <div style="width: 1024px; margin: 30px auto; position: relative; display: inline-block;">
    	<div style="width: 460px; border: 1px solid grey; padding: 20px; display: block; float: left;">
			<form method="POST" action="anime-loads-dl-manual.php">
				<div class="mb-3" style="text-align: left;">
					<label for="animeTitel" class="form-label">Titel von Film oder Serie auf Anime-Loads.org:</label>
					<input type="text" class="form-control" name="animeTitel" id="animeTitel" placeholder="Super cooler kawaii Anime <3" value="<?php echo $_POST['animeTitel'] ?>">
			
					<label for="languageselect" class="form-label">Sprache:</label>
					<select class="form-select" id="languageselect" name="languageselect" aria-label="Sprache">
						<option value="german" <?php echo (!isset($_POST['languageselect']) || $_POST['languageselect'] == 'german' ? 'selected' : '') ?>>Deutsch</option>
						<option value="japanese" <?php echo ($_POST['languageselect'] == 'japanese' ? 'selected' : '') ?>>Japanisch</option>
					</select>
			
					<label for="resolutionselect" class="form-label">Aufl&ouml;sung:</label>
					<select class="form-select" id="resolutionselect" name="resolutionselect" aria-label="Auflösung">
						<option value="1080p" <?php echo (!isset($_POST['resolutionselect']) || $_POST['resolutionselect'] == '1080p' ? 'selected' : '') ?>>1080p</option>
						<option value="720p" <?php echo ($_POST['resolutionselect'] == '720p' ? 'selected' : '') ?>>720p</option>
					</select> 
			
			
					<label for="forceAnimeResult" class="form-label">(optional) Erzwinge Anime Ergebnis Nummer:</label>
					<input type="text" class="form-control" name="forceAnimeResult" id="forceAnimeResult" placeholder="1" value="<?php echo $_POST['forceAnimeResult'] ?>"
			
					<label for="forceAnimeRelease" class="form-label">(optional) Erzwinge Release Nummer:</label>
					<input type="text" class="form-control" name="forceAnimeRelease" id="forceAnimeRelease" placeholder="1" value="<?php echo $_POST['forceAnimeRelease'] ?>">
			
			
					<div class="form-check" style="margin-bottom: 20px;">
					  <input class="form-check-input" type="checkbox" value="" id="DRYRUN" name="DRYRUN" <?php echo (isset($_POST['DRYRUN']) ? 'checked' : '') ?>>
					  <label class="form-check-label" for="DRYRUN" style="margin-left: 5px;">
						DRY RUN (Prozessausgabe aber kein Download Start)
					  </label>
					</div>
			
			
			
		  
					<button type="submit" value="Submit" class="btn btn-success">Anfragen</button>
					<!-- Button trigger modal -->
					<a href="https://www.anime-loads.org/" class="btn btn-primary" target="_blank">
					  Zeige Anime-Loads.org
					</a>
				</div>
			</form>
		</div>
		<div id="downloaded-files" style="width: 558px; max-height: 606px; overflow: auto; border: 1px solid grey; padding: 20px; display: block; float: right; text-align: left;">
			<p style="color: grey; font-size: 14px;">Downloads werden automatisch verschoben, wenn die neuste Datei &auml;lter als 10 Minuten ist und keine .rar Datei mehr existiert.<br><br>Hinzugef&uuml;gte Downloads starten innerhalb von 10 Minuten!</p>
			<p class="form-label" style="width: 100%; display: block;">Dateien im Downloads Ordner:</p>
			<div id="downloaded-files-data" style="display: block; font-size: 12px;"></div>
		</div>
	</div>
    
    
    <?php
    
    $running = false;
    $pids=trim(shell_exec("ps ux | grep 'download_anime.py' | grep -v grep"));
	if($pids == '') {
		$running = false;
	} else {
		$running = true;
		echo '<div id="processRunning" class="alert alert-danger" role="alert">A process is running! Next request is possible as soon as the current process ends.</div>';
	}
    
    
    
    echo'<h5>Anfrage Prozess Output:</h5>';
    echo '<div id="manualOutput">';
    if ($running == false && isset($_POST['animeTitel']) && $_POST['animeTitel'] != '')
    {
	$animeTitel = $_POST['animeTitel'];
	$animeTitel = preg_replace('/[^A-Za-z0-9]/', ' ', $animeTitel);
	$animeTitel = trim($animeTitel);
	$languageselect = $_POST['languageselect'];
	$resolutionselect = $_POST['resolutionselect'];
    	
    	$forceAnimeResult = ' 0';
    	if (isset($_POST['forceAnimeResult']) && $_POST['forceAnimeResult'] != '') {
    		$forceAnimeResult = ' ' . $_POST['forceAnimeResult'];
    	}
    	
    	$forceAnimeRelease = ' 0';
    	if (isset($_POST['forceAnimeRelease']) && $_POST['forceAnimeRelease'] != '') {
    		$forceAnimeRelease = ' ' . $_POST['forceAnimeRelease'];
    	}
    	
    	$DRYRUN = ' 0';
    	if(isset($_POST['DRYRUN']))
  			$DRYRUN = ' 1';
    	
    	file_put_contents($pathManualOutputLog, '');
		
    	$result = liveExecuteCommand('cd ' . $download_anime_python_dir . ';PATH=/usr/local/bin:$PATH python3 -u download_anime.py "' . $animeTitel . '" ' . $languageselect . ' ' . $resolutionselect . $forceAnimeResult . $forceAnimeRelease . $DRYRUN . ' > ' . $pathManualOutputLog . ' 2>&1 &');
		if($result['exit_status'] === 0){
		   // do something if command execution succeeds
		   if(isset($_POST['DRYRUN'])) {
		       file_put_contents($pathManualOutputLog, "DRY RUN (KEIN DOWNLOAD) Prozess gestartet [" . $animeTitel . "]... Es dauert etwa 60 Sekunden bis es weiter geht...");
		   } else {
		       file_put_contents($pathManualOutputLog, "Prozess gestartet [" . $animeTitel . "]... Es dauert etwa 60 Sekunden bis es weiter geht...");
		   }
		   
		} else {
		    // do something on failure
		    file_put_contents($pathManualOutputLog, "Prozess konnte nicht gestartet werden!");
		}
    }
    
    echo '</div>';
    
    echo '<br><br>';
    echo'<h5>Gefundene, hinzugef&uuml;gte und beobachtete Titel (neuste oben) (ani.json):</h5>';
    echo '<pre id="anijson">';
    
    $data = explode("\n",explode('"settings":', file_get_contents( $pathAniJson ))[0]);
	foreach(array_reverse($data) as $value) { 
	    echo $value."\n";
	}
    
	echo '</pre>';
	
    echo '<br><br>';
    echo '<br><br>';
    echo '<br><br>';
    
    echo '<h3>Logs f&uuml;r automatische Requests verarbeitung und anisearch.de "popular top 20" Parsing:</h3>';
    echo'<h6 style="color: red;">Nicht f&uuml;r das manuelle suchen und hinzuf&uuml;gen von dieser Seite!</h6>';
    echo '<br><br>';
    echo'<h5>downloading_and_monitoring.txt:</h5>';
    echo '<pre id="log1">';
    echo file_get_contents( $pathDownloadAndMonitoring ); // get the contents, and echo it out.
	echo '</pre>';
    echo '<br><br>';
    echo'<h5>no_releases_found_log.txt:</h5>';
    echo '<pre id="log2">';
    echo file_get_contents( $pathNoReleasesFound ); // get the contents, and echo it out.
	echo '</pre>';
	echo '<br><br>';
	echo '<br><br>';
	echo '<br><br>';
    
    
}
else
{
    ?>
	
            <form method="POST" action="anime-loads-dl-manual.php" style="width: 500px; border: 1px solid #333333; padding: 20px; margin: 100px auto;">
	            Username:<br><input type="text" name="user" class="form-control"></input><br/>
	            Passwort:<br><input type="password" name="pass" class="form-control"></input><br/>
	            <input type="submit" name="submit" value="Login" class="btn btn-success" style="margin-top: 5px;"></input>
            </form>
    <?
    
}











/**
 * Execute the given command by displaying console output live to the user.
 *  @param  string  cmd          :  command to be executed
 *  @return array   exit_status  :  exit status of the executed command
 *                  output       :  console output of the executed command
 */
function liveExecuteCommand($cmd)
{

    while (@ ob_end_flush()); // end all output buffers if any

    $proc = popen("$cmd 2>&1 ; echo Exit status : $?", 'r');

    $live_output     = "";
    $complete_output = "";

    while (!feof($proc))
    {
        $live_output     = fread($proc, 4096);
        $complete_output = $complete_output . $live_output;
        //echo "$live_output";
        @ flush();
    }

    pclose($proc);

    // get exit status
    preg_match('/[0-9]+$/', $complete_output, $matches);

    // return exit status and intended output
    return array (
                    'exit_status'  => intval($matches[0]),
                    'output'       => str_replace("Exit status : " . $matches[0], '', $complete_output)
                 );
}





?>




	</body>
</html>
