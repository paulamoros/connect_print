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

    <style>
        .nouveau-bouton {
            display: none;
        }
    </style>


    <script>
        function afficherMessage() {
            var inputFile = document.querySelector('input[type="file"]');
            var message = "";
            var extension = fichier.name.split(".").pop().toLowerCase();
            
            if (inputFile.files.length === 0) {
                message = "Veuillez sélectionner un fichier.";
            } else {
                var fichier = inputFile.files[0];
                if (fichier.size === 0) {
                    message = "Le fichier est vide.";
                
                elseif (extension !== "g") {
                    message = "Seuls les fichiers G-code (.g) sont acceptés.";
                
                } elseif (fichier.size > 5 * 1024) {
                    message = "Le fichier dépasse les 5 Mo maximums autorisés."
                } else {
                    message = "Le fichier a été téléchargé avec succès !";
                }
            }
            alert(message);
        }
        
        
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
            <h6>Command your printer</h6>
            
                <form action="" method="POST" enctype="multipart/form-data">
                    <input type="file" name="fichier" />
                    <input type="submit" value="Uploader" onclick="afficherMessage()" />
                </form>
                    
                
                
                <?php

                $afficherNouveauBouton = false;

                if(isset($_FILES['fichier'])) {
                    $nomFichier = $_FILES['fichier']['name'];
                    $nomTemporaire = $_FILES['fichier']['tmp_name'];
                    $destination = "uploads/" . $nomFichier;
                    $message = "";
                    
                    $extension = strtolower(pathinfo($nomFichier, PATHINFO_EXTENSION));
                    
                    if($extension != "g") {
                        $message = "Seuls les fichiers G-code (.g) sont autorisés.";
                        echo "Seuls les fichiers G-code (.g) sont autorisés.";
                    } elseif ($_FILES['fichier']['size'] >= 5 * 1024 * 1024) {
                        $message = "La taille du fichier dépasse la limite autorisée.";
                        echo "La taille du fichier dépasse la limite autorisée.";
                    } elseif(move_uploaded_file($nomTemporaire, $destination)) {
                        $afficherNouveauBouton =  true;
                        echo "Le fichier a été correctement téléchargé.\n";
                    } else {
                        echo "Un problème lors de l'upload est survenu.";    
                    }
                } 
                ?>
                <?php
                if ($afficherNouveauBouton) {
                    ?>
                    <button onclick="redirection()"> Accéder à l'interface de l'imprimante</button>
                    <?php
                }
                ?>
                
                <script>
                function redirection() {
                    window.location.href = "interface.php";
                }
                </script>
          </div>
        </div>
      </div>
    </div>
  </div>

</body>
</html>