<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

<title>Parc 3D controller</title>

<!-- Bootstrap core CSS -->
<link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">


<!-- Additional CSS Files -->
<link rel="stylesheet" href="assets/css/templatemo-tale-seo-agency.css">

</head>

<body>

<!-- ***** Header Area Start ***** -->
<header class="header-area header-sticky">
<div class="container">
<div class="row">
<div class="col-10">
<nav class="main-nav">
<!-- ***** Logo Start ***** -->
<a href="index.php" class="logo">
<img src="assets/images/logo.png" alt="" style="max-width: 1012px;">
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
<h6>Command your printing</h6>
<div class="line-dec"></div>
<h4>Select <em>your printer</em> to begin <span></span></h4>
<p>You would be allow to get informations and print your own design, do everything from your computer</a>.</p>
<style>
select {
background-color: #228B22;
color: #FFFFFF;
font-size: 16px;
padding: 8px 16px;
border: none;
border-radius: 4px;
cursor: pointer;
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

</style>
<form action="" method="POST">
<select name="printer_nb">
<option value="0">Printer 0</option>
<?php
$option = $_POST['printer_nb'];
$redirections = array(
'0' => 'd_imprimante0/imprimante.php',
// options ajoutées automatiquement par setup.py
);

if (array_key_exists($option, $redirections)) {
$url = $redirections[$option];
header('Location: ' . $url);
exit;
} elseif ($option != '' && basename($_SERVER['PHP_SELF']) != 'index.php') {
header('Location: index.php');
exit;
} else {
echo 'Redirection non valide';
}

?>
</select>
<button type="submit">Let's go</button>
</form>

</div>
</div>
</div>
</div>
</div>
