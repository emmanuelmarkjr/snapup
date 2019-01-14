<?php

/* 
 * Author: Mark Emmanuel
 * Phone: +2348111306490
 * Email: mebuilds1@gmail.com
 */
include 'params/params.php';
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <title>TOMF || Home Page</title>

    <link rel="shortcut icon" type="image/png" href="<?php echo $site_root."/assets/"?>images/fevicon.png">
    <link href="https://fonts.googleapis.com/css?family=Rubik:300,300i,400,400i,500,500i,700,700i,900,900i" rel="stylesheet">
    <link href="<?php echo $site_root."/assets/"?>css/animate.min.css" rel="stylesheet" type="text/css">
    <link href="<?php echo $site_root."/assets/"?>css/bootstrap.min.css" rel="stylesheet" type="text/css">
     <link href="<?php echo $site_root."/assets/"?>css/font-awesome.min.css" rel="stylesheet" type="text/css">
    <link href="<?php echo $site_root."/assets/"?>css/meanmenu.css" rel="stylesheet" type="text/css">
    <link href="<?php echo $site_root."/assets/"?>css/hover-min.css" rel="stylesheet" type="text/css">
    <link href="<?php echo $site_root."/assets/"?>css/font-awesome.css" rel="stylesheet" type="text/css">
    <link href="<?php echo $site_root."/assets/"?>css/bar.css" rel="stylesheet" type="text/css">
    <link href="<?php echo $site_root."/assets/"?>css/owl.carousel.css" rel="stylesheet" type="text/css">
    <link href="<?php echo $site_root."/assets/"?>css/custom/style.css" rel="stylesheet" type="text/css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/sweetalert/1.1.3/sweetalert.min.css" rel="stylesheet" type="text/css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/sweetalert/1.1.3/sweetalert.min.js"></script>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
</head>

<body class="about">
    <?php include 'includes/header.php'; ?>
    <div class="romana_allPage_area">
        <div class="container">
            <div class="row">
                <div class="col-xs-12">
                    <div class="romana_allPage_text wow zoomIn">
                        <h1>About us</h1>
                        <ol class="breadcrumb">
                            <li><a href="/">Home</a><span></span></li>
                            <li class="active"><a href="#">about</a></li>
                        </ol>
                    </div>
                </div>
                <!-- column End -->
            </div>
            <!-- row End -->
        </div>
        <!-- container End -->
    </div>
<!-- ==========================================================
*Mission_area start
============================================================ -->
    <?php

        $dbhost  = "localhost";
        $dbuser  = "gqabzbdzvu";
        $dbpass   = "FS4hTPepkT";           
        $conn = mysql_connect($dbhost, $dbuser, $dbpass) or die ('Error connecting to mysql');
        

        $dbname   = "gqabzbdzvu";
        mysql_select_db($dbname);

        $query = "SELECT page_content FROM pages WHERE page_name='what_we_do'";
        $result = mysql_query($query) 
        or die(mysql_error()); 
        $row = mysql_fetch_array($result, MYSQL_ASSOC)
            ?>
    <div class="romana_mission_area spt100">
        <div class="container">
            <div class="row">
                <div class="col-sm-4">
                    <div class="mission_img">
                        <img src="images/mission_img.jpg" alt="">
                    </div>
                </div>
                <div class="col-sm-8">
                    <div class="mission_text">
                        <h2>What We Do</h2>
                        <?php echo "<p>" . $row['page_content']  . "</p>"; ?>
                        </div>
                </div>
                <!-- column End -->
            </div>
            <!-- row End -->
        </div>
        <!-- container End -->
    </div>
<!-- ==========================================================
*romana_save_life_area start
============================================================ -->
  
<!-- ==========================================================
*romana_cta_area start
============================================================ -->
    <div class="romana_cta_area mt66">
        <div class="container">
            <div class="row ">
                <div class="col-md-8 col-md-offset-1 col-sm-9">
                    <h2>Lest make the world better togethers.</h2>
                </div>
                <!-- column End -->
                <div class="col-sm-3">
                    <a href="volunteer.php" class="hvr-box-shadow-outset common_btn">join with us<i class="fa fa-long-arrow-right"></i></a>
                </div>
                <!-- column End -->
            </div>
            <!-- row End -->
        </div>
    </div>
<?php include 'includes/footer.php'; ?>
</body>
</html>

