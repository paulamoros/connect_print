<?php
session_start();
?>
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


  </head>

<body>

  <!-- ***** Header Area Start ***** -->
  <header class="header-area header-sticky">
    <div class="container">
        <div class="row">
            <div class="col-10">
                <nav class="main-nav">
                    <!-- ***** Logo Start ***** -->
                    <a href="index.html" class="logo">
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
            <h6>Command your printer</h6>
            <div class="line-dec"></div>
			            <!-- Here is the form that will transmit the archive of the user to the php-file-handling script. 
            The not-to-forget parts are : 
            - enctype property set to "multipart/form-data" -->
	<form action="upload.php" method="post" enctype="multipart/form-data">
			Select a GCODE to upload:
		<input type="file" name="fileToUpload" id="fileToUpload">
		<input type="submit" value="Upload gcode" name="submit">
      </form>
		<?php
		if($_SESSION["return"] == null) {
		}else{
			echo $_SESSION["return"];
		}
		?>

          </div>
        </div>
      </div>
    </div>
  </div>

<div id="FileUpload">
  <div class="wrapper w-100 bg-light p-3 rounded">
    <div class="upload">
	
    </div>
  </div>
</div>

</body>
