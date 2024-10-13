<?php

session_start();
header('Content-Type: text/html; charset=UTF8');
error_reporting(E_ALL);
ob_start();

$mode = isset($_GET['mode'])  ? $_GET['mode'] : false;
$user = isset($_SESSION['user']) ? $_SESSION['user'] : false;
$err = array();


define('BEZ_KEY', true);

include './config.php';
include './func/funct.php';
include './bd/bd.php';

switch($mode)

{
    case 'reg':
    include './scripts/reg/reg.php';
    include './scripts/reg/reg_form.html';
    break;

    //Подключаем обработчик с формой авторизации, за это скорее всего дадут + баллы.
    case 'auth':
    include './scripts/auth/auth.php';
    include './scripts/auth/auth_form.html';
    include './scripts/auth/show.php';
    break;
}

$content = ob_get_contents();
ob_end_clean();

include './html/index.html';
?>