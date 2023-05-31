<!DOCTYPE html>
<html lang="en">

  <head>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

    <title>Parc 3D controller</title>

    <!-- Bootstrap core CSS -->
    <link href="../vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">


    <!-- Additional CSS Files -->

    <link rel="stylesheet" href="../assets/css/templatemo-tale-seo-agency.css">

    
    
    <script>
        function mettreAJourContenu() {
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    var nouveauContenu = xhr.responseText;
                    document.getElementById("contenu").textContent = nouveauContenu;
                }
            };
            xhr.open("GET", "status.txt", true);
            xhr.send();
        }

        // Effectuer la mise à jour périodique toutes les 5 secondes
        setInterval(mettreAJourContenu, 5000);
        
        function timer_update(){
            fetch('timer.txt')
                .then(response => response.text())
                .then(contenu => {
                    document.getElementById('contenuFichier').textContent = contenu;
                })
                .catch(error => {
                    console.log('Erreur :', error);
                });
        }
        setInterval(timer_update, 1000);
        
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
                    <a href="../index.html" class="logo">
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
            <div id="contenu"></div>
            
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
            </div>
            
            <h6>Piece to print informations</h6>
            
            <?php            
            $output = shell_exec('python piece_information.py');
            echo "<pre>$output</pre>";
            ?>
            
            </div>
            
            <div id="contenuFichier"></div>
            
            <form action="" method='POST'>
            <button class="button" type="submit" name="script" value="print">Start printing</button>
            <button class="button" type="submit" name="script" value="emergency_stop">Process kill</button>
            <button class="button" type="submit" name="script" value="pause">Pause printing</button>
            <button class="button" type="submit" name="script" value="resume">Resume printing</button>
            </form>
            <?php
            if ($_SERVER['REQUEST_METHOD'] === 'POST') {
                $script = $_POST['script'];
                
                if ($script === 'print') {
                    shell_exec('python print*.py &');
                }
                if ($script === 'emergency_stop') {
                    shell_exec('emergency_stop.py');
                }
            }
            ?>
            
            
            
        </div>
      </div>
    </div>
  </div>

</body>
</html>

