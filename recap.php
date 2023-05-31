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
   
        function convertNewlinesToBreaks(text) {
            return text.replace(/\n/g, '<br>');
        }
        function getFileContent() {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var fileContent = this.responseText;
                    var formattedContent = convertNewlinesToBreaks(fileContent);
                    document.getElementById('fileContent').innerHTML = formattedContent;
                }
            };
            xhttp.open('GET', 'recap.txt', true);
            xhttp.send();
        }

        setInterval(getFileContent, 1000);
    </script>

    <?php
        shell_exec('python /var/www/html/recap.py')
    ?>
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
                        <img src="../assets/images/logo.png" alt="" style="max-width: 1012px;">
                    </a>
                    <!-- ***** Logo End ***** -->
                </nav>
            </div>
        </div>
    </div>
    
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

  </header>
  <!-- ***** Header Area End ***** -->

  <div class="main-banner" id="top">
    <div class="container">
      <div class="row">
        <div class="col-lg-7">
          <div class="caption header-text">
          
            <button class="button"><a style="color: white; text-decoration: none;" href="index.php">Back to printer selection page</a></button>
            <br>
            <br>
            <br>
            <h6>Global view of the 3D printer fleet</h6>    
            <br>
            <div id="fileContent"></div>
            
        </div>
      </div>
    </div>
  </div>

</body>
</html>


