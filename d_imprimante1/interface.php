<!DOCTYPE html>
<html lang="en">

  <head>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

    <title>Parc 3D controller</title>

    <!-- Additional CSS Files -->
    <link rel="stylesheet" href="../assets/css/templatemo-tale-seo-agency.css">

    
    
    <script>        
        
        function convertNewlinesToBreaks(text) {
            return text.replace(/\n/g, '<br>');
        }
        function getStatus() {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var fileContent = this.responseText;
                    var formattedContent = convertNewlinesToBreaks(fileContent);
                    document.getElementById('StatusContent').innerHTML = formattedContent;
                }
            };
            xhttp.open('GET', 'status.txt', true);
            xhttp.send();
        }
        
        function getTimer() {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var fileContent = this.responseText;
                    var formattedContent = convertNewlinesToBreaks(fileContent);
                    document.getElementById('TimerContent').innerHTML = formattedContent;
                }
            };
            xhttp.open('GET', 'timer.txt', true);
            xhttp.send();
        }

        setInterval(getStatus, 1000);
        setInterval(getTimer, 1000);
        
        
        
        
    </script>
    
    </head>

    <body>

  <!-- ***** Header Area Start ***** -->
  <header class="header-area header-sticky">
    <div class="container">
        <div class="row">
            <div class="col-10">
                <nav class="main-nav">
                    <!-- ***** Logo Start ***** -->
                    <a href="../index.php" class="logo">
                        <img src="../assets/images/logo.png" alt="" style="max-width: 1012px;">
                    </a>
                    <!-- ***** Logo End ***** -->
                </nav>
            </div>
        </div>
    </div>
  </header>
  <!-- ***** Header Area End ***** -->

  <div class="main-banner" id="top">
    <div class="container">
      <div class="row">
        <div class="col-lg-7">
        
          <div class="caption header-text">
            <h6>Printer informations</h6>
            
            <h1>Printer status:</h1>
            
            <div id="StatusContent"></div>
            
            <style>
                button {
                background-color: #228B22;
                color: #FFFFFF;
                font-size: 16px;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                }
            </style>
            <br> <br>
            <h6>Piece to print informations</h6>
            
            <?php            
            $output = shell_exec('python piece_information.py');
            echo "<pre>$output</pre>";
            ?>
            
            <div id="TimerContent"></div>
            <br> <br>
            <h6>Temperature graph</h6>
            <iframe id="graph-frame" src="graph.html" width="800" height="600"></iframe>
            
            <?php
            $output = shell_exec('ipython data1.py > /dev/null 2>&1 &');
            ?>
            
            <form action="" method='POST'>
                <button class="button" type="submit" name="script" value="print">Start printing</button>
                <button class="button" type="submit" name="script" value="emergency_stop">Stop printing (irreversible)</button>
                <button class="button" type="submit" name="script" value="pause_resume">Pause/Resume printing</button>
                <button class="button" type="submit" name="script" value="clean">Printer cleaned</button>
            </form>
          </div>
        </div>
        
        <div class="console">
          <pre>
              <?php
              
                if ($_SERVER['REQUEST_METHOD'] === 'POST') {
                    $script = $_POST['script'];
                    
                    
                    if ($script === 'print') {
                        $output_print = shell_exec('python print1.py > /dev/null 2>&1 &');
                        $output_print = nl2br($output_print);
                        $output_timer = shell_exec('python timer1.py > /dev/null 2>&1 &');
                        $output_timer = nl2br($output_timer);
                    }
                    if ($script === 'emergency_stop') {
                        shell_exec('python control_printer.py stop');
                    }
                    if ($script === 'pause_resume') {
                        shell_exec('python control_printer.py pause');
                    }
                    if ($script === 'clean') {
                        shell_exec('python control_printer.py clean');
                    }
                }
                ?>
          </pre>
          
        </div>
      </div>
    </div>
  </div>

</body>
</html>


