<?php
    
     if(!defined('BEZ_KEY'))
     {
         header("HTTP/1.1 404 Not Found");
         exit(file_get_contents('./../../404.html'));
     }

    
     if(isset($_POST['submit']))
     {
        if(empty($_POST['email']))
            $err[] = 'Не введен Логин';

        if(empty($_POST['pass']))
            $err[] = 'Не введен Пароль';

        
        if(count($err) > 0)
            echo showErrorMessage($err);
        else
        {
            
            $sql = 'SELECT *
                    FROM `'. BEZ_DBPREFIX .'reg`
                    WHERE `login` = "'. escape_str($_POST['email']) .'"
                    AND `status` = 1';
            $res = mysqlQuery($sql);

            
            if(mysql_num_rows($res) > 0)
            {
                
                $row = mysql_fetch_assoc($res);

                if(md5(md5($_POST['pass']).$row['salt']) == $row['pass'])
                {
                    $_SESSION['user'] = true;

                    
                    header('Location:'. BEZ_HOST .'less/reg/?mode=auth');
                    exit;
                }
                else
                    echo showErrorMessage('Неверный пароль!');
            }
            else
                echo showErrorMessage('Логин <b>'. $_POST['email'] .'</b> не найден!');
        }

     }

    ?>