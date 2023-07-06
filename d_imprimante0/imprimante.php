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
        
        button {
            background-color: #228B22;
            color: #FFFFFF;
            font-size: 16px;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .choisir-fichier {
            background-color: #228B22;
            color: #FFFFFF;
            font-size: 16px;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
    </style>


    <script>
        function afficherMessage() {
            var inputFile = document.querySelector('input[type="file"]');
            var message = "";
            var extension = fichier.name.split(".").pop().toLowerCase();
            var fichier = inputFile.files[0];
            
            if (inputFile.files.length === 0) {
                message = "Please choose a g-file.";
            } else {
                
                if (fichier.size === 0) {
                    message = "File is empty.";
                
                } else if (extension !== "g") {
                    message = "Only g-code file (.g) are allowed.";
                
                } else if (fichier.size > 5 * 1024) {
                    message = "The file exceeds the 5 Mo authorized.";
                
                } else {
                    message = "File successfuly downloaded !";
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
            <h6>Command your printer</h6>
            
                <form action="" method="POST" enctype="multipart/form-data">
                    <input type="file" name="fichier" class="button choisir-fichier" />
                    <input type="submit" value="Uploader" onclick="afficherMessage()" class="button"/>
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
                        $message = "Only g-code files (.g) are allowed.";
                        echo "Seuls les fichiers G-code (.g) sont autorisés.";
                    } elseif ($_FILES['fichier']['size'] >= 5 * 1024 * 1024) {
                        $message = "The file size is too big.";
                        echo "The file size is too big.";
                    } elseif(move_uploaded_file($nomTemporaire, $destination)) {
                        $afficherNouveauBouton =  true;
                        echo "File downloaded successfuly.\n";
                    } else {
                        echo "An issue happened during the upload.";    
                    }
                } 
                ?>
                <?php
                if ($afficherNouveauBouton) {
                    ?>
                    <br>
                    <button onclick="redirection()" class="button"> Go to printer interface</button>
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