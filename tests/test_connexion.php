<?php

session_start();

$connexion = mysqli_connect('localhost','db_user','password','users');

if (!$connexion) {
    $error_message = "Erreur de connexion à la base de données " . mysqli_connect_error();
} else {
    $username = $_POST['username'];
    $password = $_POST['password'];

    $query = "SELECT * FROM utilisateurs WHERE username = '$username'";
    $result = mysqli_query($connexion, $query);

    if(mysqli_num_rows($result) == 1) {
        $user = mysqli_fetch_assoc($result);
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['username'] = $user['nom_utilisateur'];
    
        header('Location: /var/www/html/index.php');
        exit();

    } else {
        $error_message = "Identifiants invalides";
    }
    mysqli_close($connexion);
}
?>

<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>Page de connexion</title>
</head>
<body>
	<h2>Connexion</h2>
	<?php if (isset($error_message)): ?>
    	<p><?php echo $error_message; ?></p>
	<?php endif; ?>
	<form method="post" action="login.php">
    	<div>
        	<label for="username">Nom d'utilisateur :</label>
        	<input type="text" id="username" name="username" required>
    	</div>
    	<div>
        	<label for="password">Mot de passe :</label>
        	<input type="password" id="password" name="password" required>
    	</div>
    	<div>
        	<input type="submit" value="Se connecter">
    	</div>
	</form>
</body>
</html>



