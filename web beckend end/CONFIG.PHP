<?php



     if(!defined('BEZ_KEY'))
     {
         header("HTTP/1.1 404 Not Found");
         exit(file_get_contents('./404.html'));
     }

    
     define('BEZ_DBSERVER','localhost');

     //логины
     define('BEZ_DBUSER','');

     //пасворд
     define('BEZ_DBPASSWORD','');

     //БД
     define('BEZ_DATABASE','');

     //кост бд
     define('BEZ_DBPREFIX','bez_');

     //ошибки
     define('BEZ_ERROR_CONNECT','Немогу соеденится с БД');

    //ошибки
     define('BEZ_NO_DB_SELECT','Данная БД отсутствует на сервере');

     //Адрес хоста сайта
     define('BEZ_HOST','http://'. $_SERVER['HTTP_HOST'] .'/');

     //Адрес почты от кого отправляем
     define('BEZ_MAIL_AUTOR','Регистрация на urlnashegosaita.com <thrillpill821@gmail.com');
     ?>