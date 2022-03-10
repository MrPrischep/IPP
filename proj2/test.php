<?php

$paramsError = 10; // parameter is missing
$inputFileError = 11;   // error loading input file
$outputFileError = 12;   // error loading output file
$internalError = 99;   // sth went horribly wrong
$lexikalError = 21;   // lexical or syntax error

$directory = "./";
$parse = "./parse.php";
$interpret = "./interpret.py";
$jexamxml = '/pub/courses/ipp/jexamxml/jexamxml.jar';
$jexamcfg = '/pub/courses/ipp/jexamxml/options';

$recursiveFlag = 0;
$directoryFlag = 0;
$parseFlag = 0;
$intFlag = 0;
$parseOnlyFlag = 0;
$intOnlyFlag = 0;
$jexamxmlFlag = 0;
$jexamcfgFlag = 0;

$counterOfParams = count($argv);


$myOpt = "";
$options = array("help", "directory:", "recursive", "parse-script:", "int-script:", 
                 "parse-only", "int-only", "jexamxml:", "jexamcfg:");
$getOptions = getopt($myOpt, $options);
var_dump($getOptions);

if (array_key_exists("help", $getOptions)) {
    if (($counterOfParams == 2) && ($argv[1] == "--help")) {
        echo ("'--directory=path' : tests will search in the specified directory\n");
        echo ("'--recursive' tests will search not only in the specified directory but also recursively in all its subdirectories\n");
        echo ("'--parse-script=file' script file in PHP 7.4 for source code analysis in IPP-code21 \n");
        echo ("'--int-script=file' script file in Python 3.8 for the XML code representation interpreter in IPPcode21\n");
        echo ("'--parse-only' will only test the source code parsing script in IPPcode21 (this parameter must not be combined with parameters --int-only and --int-script)\n");
        echo ("'--int-only' only the script for the XML code representation interpreter in IPPcode21 will be tested (this parameter must not be combined with the --parse-only and --parse-script parameters)\n");
        echo ("'--jexamxml=file' file with JAR package with A7Soft JExamXML tool\n");
        echo ("'--jexamcfg=file' A7Soft JExamXML configuration file\n");
        exit(0);

    } else {
        exit($paramsError);
    }
}

if (array_key_exists("directory", $getOptions)) {
    $directoryFlag = 1;
    $directory = $getOptions["directory"];
    #echo($directoryFlag);
    echo("$directory\n");
} 

if (array_key_exists("recursive", $getOptions)) {
    $recursiveFlag = 1;
}

if (array_key_exists("parse-script", $getOptions)) {
    $parseFlag = 1;
    $parse = $getOptions["parse-script"];
    echo($parse);
}

if (array_key_exists("int-script", $getOptions)) {
    $intFlag = 1;
    $interpret = $getOptions["int-script"];
    echo($interpret);
}

if (array_key_exists("parse-only", $getOptions)) {
    $parseOnlyFlag = 1;
}

if (array_key_exists("int-only", $getOptions)) {
    $intOnlyFlag = 1;
}

if (array_key_exists("jexamxml", $getOptions)) {
    $jexamxmlFlag = 1;
}

if (array_key_exists("jexamcfg", $getOptions)) {
    $jexamcfgFlag = 1;
}

if (($parseOnlyFlag == 1 and $intOnlyFlag == 1) or ($parseOnlyFlag == 1 and $intFlag == 1)) {
    fprintf(STDERR, "Parameter --parse-only can not kombined with parameteres --int-only and --int-script\n");
    exit(10);
}

if (($intOnlyFlag == 1 and $parseOnlyFlag == 1) or ($intOnlyFlag == 1 and $parseFlag == 1)) {
    fprintf(STDERR, "Parameter --int-only can not kombined with parameteres --parse-only and --parse-script\n");
    exit(10);
}

if (file_exists($directory) == false) {
    fprintf(STDERR, "Bad directory\n");
    exit($inputFileError);
}

if (file_exists($parse) == false) {
    fprintf(STDERR, "Bad input parse file\n");
    exit($inputFileError);
}

if (file_exists($interpret) == false) {
    fprintf(STDERR, "Bad input interpret file\n");
    exit($inputFileError);
}

if ($recursiveFlag == 1) {
    exec("find " . $directory . " -regex '.*\.src$'", $path);
} else {
    exec("find " . $directory . " -maxdepth 1 -regex '.*\.src$'", $path);
}