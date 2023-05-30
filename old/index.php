<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 1.0 Transitional//EN"
"http://www.org/xhtml/html-transitional.dtd">
<?php
$printer_nb = $_POST['printer_nb'];
$printer_page = d_imprimante.$_POST['printer_nb']."/imprimante.php";

echo "<p><a href=$printer_page>Accéder à la page de l'imprimante</a></p>";
?>
