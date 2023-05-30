<?php

if(isset($_FILES['fichier'])) {
    $nomFichier = $_FILES['fichier']['name'];
    $nomtemporaire = $_FILES['fichier']['tmp_name'];
    $destination = "uploads/" . $nomFichier;
    
    if(move_uploaded_file($nomTemporaire, $destination)) {
        echo "Le fichier a été téléchargé avec succès.";
    } else {
        echo "Une erreur s'est lors du téléchargement du fichier.";
        $_SESSION["return"] =  "Sorry, your file is too large.";
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Uploader un fichier</title>
</head>
<body>
    <form action="" method="POST" enctype="multipart/form-data">
        <input type="file" name="fichier" />
        <input type="submit" value="Uploader" />
    </form>
</body>
</html>