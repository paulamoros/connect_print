<?php
session_start();

$target_dir = "./";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));

// Check if file already exists
if (file_exists($target_file)) {
  shell_exec("rm $target_file ");
  //$_SESSION["return"] = "Sorry, file already exists.";
  //$uploadOk = 0;
}

// Check file size
if ($_FILES["fileToUpload"]["size"] > 500000) {
  $_SESSION["return"] =  "Sorry, your file is too large.";
  $uploadOk = 0;
}

// Allow certain file formats
if($imageFileType != "g") {
  $_SESSION["return"] = "Sorry, only GCODE (.g) files are allowed.";
  $uploadOk = 0;
}

// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
  echo "Sorry, your file was not uploaded.";
// if everything is ok, try to upload file
header("Location: imprimante.php");

} else {
  if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)){
    echo "The file ". htmlspecialchars( basename( $_FILES["fileToUpload"]["name"])). " has been uploaded.";
 	$_SESSION["file_name"] = $target_file;
	header("Location: imprimer.php");
  } else {
    echo "Sorry, there was an error uploading your file.";
	header("Location: imprimante.php");
  }
}
?>
