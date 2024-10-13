<?php
   
    

     
     if(!defined('BEZ_KEY'))
     {
         header("HTTP/1.1 404 Not Found");
         exit(file_get_contents('./../404.html'));
     }

   
     function escape_str($data)
     {
        if(is_array($data))
        {
            if(get_magic_quotes_gpc())
               $strip_data = array_map("stripslashes", $data);
               $result = array_map("mysql_real_escape_string", $strip_data);
               return  $result;
        }
        else
        {
            if(get_magic_quotes_gpc())
               $data = stripslashes($data);
               $result = mysql_real_escape_string($data);
               return $result;
        }
     }

    
     function sendMessageMail($to, $from, $title, $message)
     {
       

       
       $subject = $title;
       $subject = '=?utf-8?b?'. base64_encode($subject) .'?=';

   
       $headers = "Content-type: text/html; charset=\"utf-8\"\r\n";
       $headers .= "From: ". $from ."\r\n";
       $headers .= "MIME-Version: 1.0\r\n";
       $headers .= "Date: ". date('D, d M Y h:i:s O') ."\r\n";

      
       if(!mail($to, $subject, $message, $headers))
          return 'Ошибка отправки письма!';
       else
          return true;
     }

      
     function showErrorMessage($data)
     {
        $err = '<ul>'."\n";

        if(is_array($data))
        {
            foreach($data as $val)
                $err .= '<li style="color:red;">'. $val .'</li>'."\n";
        }
        else
            $err .= '<li style="color:red;">'. $data .'</li>'."\n";

        $err .= '</ul>'."\n";

        return $err;
     }

      
     function mysqlQuery($sql)
     {
        $res = mysql_query($sql);
        

        if(!$res)
        {
            $message  = 'Неверный запрос: ' . mysql_error() . "\n";
            $message .= 'Запрос целиком: ' . $sql;
            die($message);
        }

        return $res;
     }

    
     function salt()
     {
        $salt = substr(md5(uniqid()), -8);
        return $salt;
     }