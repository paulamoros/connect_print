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
            <h6>Global view of the 3D printer fleet</h6>
            
            <table>
                <tr>
                    <th>Line 1</th>
                    <th>Line 2</th>
                </tr>
                <tr>
                    <th>Line 1</th>
                </tr>
                
                <tr>
                    <th>Line 1</th>
                </tr>
                
            </table>
            
            
            
            
            
        </div>
      </div>
    </div>
  </div>

</body>
</html>

