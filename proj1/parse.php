<?php

/* IPP 2021
 * @file parse.php
 * @author Kozhevnikov Dmitrii
*/
controlArguments();

if (!$lineOfProgram = fgets(STDIN)) {
    fprintf(STDERR, "Chyba při otevírání vstupních souborů\n");
    exit(21);
}
$lineOfProgram = explode("#", $lineOfProgram, 2);
$lineOfProgram = $lineOfProgram[0];
$lineOfProgram = trim($lineOfProgram);
$lineOfProgram = strtoupper($lineOfProgram);
checkNevalidSymbols($lineOfProgram);
while(1) {
    if ($lineOfProgram == "") {
        if (!$lineOfProgram = fgets(STDIN)) {
            exit(21);
        }
        $lineOfProgram = explode("#", $lineOfProgram, 2);
        $lineOfProgram = $lineOfProgram[0];
        $lineOfProgram = trim($lineOfProgram);
        $lineOfProgram = strtoupper($lineOfProgram);
    } else {
        break;
    }
}
//  head control
if ($lineOfProgram != ".IPPCODE21") {
    fprintf(STDERR, "Chybná nebo chybějící hlavička ve zdrojovém kódu zapsaném v IPPcode21\n");
    exit(21);
}

// XML
$doc = new DOMDocument("1.0", "UTF-8");
$doc->formatOutput = true;

// root-element
$programRoot = $doc->createElement("program");
// atribut with value IPPcode21
$language = $doc->createAttribute("language");
$language->value = "IPPcode21";
$programRoot->appendChild($language);

//  atribut order with instructions
$order = 1;
global $ccc; 
$ccc = 1;

// reading program
while ($lineOfProgram = fgets(STDIN)) {
    $lineOfInstruction = dividingLine($lineOfProgram);              // string -> array of elements
    
    $count = count($lineOfInstruction); // count of elements   
    
    // empty line control
    if ($count == null) {
        continue;
    }
    
    $instruction = $doc->createElement("instruction");
    $instructionAttribute = $doc->createAttribute("order");
    $instructionAttribute->value = $order;
    $instruction->appendChild($instructionAttribute);
    $instruction = $programRoot->appendChild($instruction);

    // control 1 valid element
    if ($count == 1) {
        if (checkForOneArg($lineOfInstruction[0])) {
            $instructionOpCode = $doc->createAttribute("opcode");
            $instructionOpCode->value = $lineOfInstruction[0];
            $instruction->appendChild($instructionOpCode);
        } else {
            fprintf(STDERR, "Unknown operator!\n");
            exit(23);
        }
    // control 2 valid elements
    } elseif ($count == 2) {                                    
        if (checkForTwoVarArg($lineOfInstruction[0])) {
            $instructionOpCode = $doc->createAttribute("opcode");
            $instructionOpCode->value = $lineOfInstruction[0];
            $instruction->appendChild($instructionOpCode);

            //  <var>
            if (isOpVar($lineOfInstruction[1])) {
                $i = 1;
                $usingType = "var";
                $arg = $doc->createElement("arg".$i);
                $instruction->appendChild($arg);
                $type = $doc->createAttribute("type");
                $type->value = $usingType;
                $arg->appendChild($type);
                $argValue = "$lineOfInstruction[1]";
                $argText = $doc->createTextNode($argValue);
                $arg->appendChild($argText);
                
            } else {
                fprintf(STDERR, "Unknown operator!\n");
                exit(23);
            }
        } elseif (checkForTwoArgSym($lineOfInstruction[0])) {
            $instructionOpCode = $doc->createAttribute("opcode");
            $instructionOpCode->value = $lineOfInstruction[0];
            $instruction->appendChild($instructionOpCode);

            //  <symb>
            if (isOpSym($lineOfInstruction[1])) {
                $i = 1;
                $arg = $doc->createElement("arg".$i);
                $instruction->appendChild($arg);
                $type = $doc->createAttribute("type");
                $type->value = $symbType;
                $arg->appendChild($type);
                $argValue = "$symbValue";
                $argText = $doc->createTextNode($argValue);
                $arg->appendChild($argText);
            }
        } elseif (checkForTwoArgLabel($lineOfInstruction[0])) {
            $instructionOpCode = $doc->createAttribute("opcode");
            $instructionOpCode->value = $lineOfInstruction[0];
            $instruction->appendChild($instructionOpCode);

            //  <label>
            if (isOpLabel($lineOfInstruction[1])) {
                $i = 1;
                $usingType = "label";
                $arg = $doc->createElement("arg".$i);
                $instruction->appendChild($arg);
                $type = $doc->createAttribute("type");
                $type->value = $usingType;
                $arg->appendChild($type);
                $argValue = "$lineOfInstruction[1]";
                $argText = $doc->createTextNode($argValue);
                $arg->appendChild($argText);
            } else {
                fprintf(STDERR, "Unknown operator!\n");
                exit(23);
            }
        } else {
            fprintf(STDERR, "Unknown operator!\n");
            exit(22);
        }
    
    // control 3 elements
    } elseif ($count == 3) {
        if (checkForThreeArg($lineOfInstruction[0])) {
            $instructionOpCode = $doc->createAttribute("opcode");
            $instructionOpCode->value = $lineOfInstruction[0];
            $instruction->appendChild($instructionOpCode);

            // <var> <type>
            if (isOpVar($lineOfInstruction[1]) && isOpType($lineOfInstruction[2])) {
                $i = 1;
                $usingType = "var";
                $arg = $doc->createElement("arg".$i);
                $instruction->appendChild($arg);
                $type = $doc->createAttribute("type");
                $type->value = $usingType;
                $arg->appendChild($type);
                $argValue = "$lineOfInstruction[1]";
                $argText = $doc->createTextNode($argValue);
                $arg->appendChild($argText);
                $i++;
                $usingType = "type";
                $arg = $doc->createElement("arg".$i);
                $instruction->appendChild($arg);
                $type = $doc->createAttribute("type");
                $type->value = $usingType;
                $arg->appendChild($type);
                $argValue = "$lineOfInstruction[2]";
                $argText = $doc->createTextNode($argValue);
                $arg->appendChild($argText);
            } else {
                fprintf(STDERR, "Unknown operator!\n");
                exit(23);
            }
        } elseif (checkForThreeArgVarSymb($lineOfInstruction[0])) {
            $instructionOpCode = $doc->createAttribute("opcode");
            $instructionOpCode->value = $lineOfInstruction[0];
            $instruction->appendChild($instructionOpCode);

            //  <var> <symb>
            if (isOpVar($lineOfInstruction[1]) && isOpSym($lineOfInstruction[2])) {
                $i = 1;
                $usingType = "var";
                $arg = $doc->createElement("arg".$i);
                $instruction->appendChild($arg);
                $type = $doc->createAttribute("type");
                $type->value = $usingType;
                $arg->appendChild($type);
                $argValue = "$lineOfInstruction[1]";
                $argText = $doc->createTextNode($argValue);
                $arg->appendChild($argText);
                $i++;
                
                $arg = $doc->createElement("arg".$i);
                $instruction->appendChild($arg);
                $type = $doc->createAttribute("type");
                $type->value = $symbType;
                $arg->appendChild($type);
                $argValue = "$symbValue";
                $argText = $doc->createTextNode($argValue);
                $arg->appendChild($argText);
            } else {
                fprintf(STDERR, "Unknown operator!\n");
                exit(23);
            }
        } else {
            fprintf(STDERR, "Unknown operator!\n");
            exit(23);
        }

    // control 4 arguments
    } elseif ($count == 4) {
        if (checkForFourVarSymSym($lineOfInstruction[0])) {
            $instructionOpCode = $doc->createAttribute("opcode");
            $instructionOpCode->value = $lineOfInstruction[0];
            $instruction->appendChild($instructionOpCode);

            //  <var> <symb> <symb>
            if (isOpVar($lineOfInstruction[1]) && isOpSym($lineOfInstruction[2])) {
                $i = 1;
                $usingType = "var";
                $arg = $doc->createElement("arg".$i);
                $instruction->appendChild($arg);
                $type = $doc->createAttribute("type");
                $type->value = $usingType;
                $arg->appendChild($type);
                $argValue = "$lineOfInstruction[1]";
                $argText = $doc->createTextNode($argValue);
                $arg->appendChild($argText);
                $i++;

                $arg = $doc->createElement("arg".$i);
                $instruction->appendChild($arg);
                $type = $doc->createAttribute("type");
                $type->value = $symbType;
                $arg->appendChild($type);
                $argValue = "$symbValue";
                $argText = $doc->createTextNode($argValue);
                $arg->appendChild($argText);

                if (isOpSym($lineOfInstruction[3])) {
                    $i = 3;
                    $arg = $doc->createElement("arg".$i);
                    $instruction->appendChild($arg);
                    $type = $doc->createAttribute("type");
                    $type->value = $symbType;
                    $arg->appendChild($type);
                    $argValue = "$symbValue";
                    $argText = $doc->createTextNode($argValue);
                    $arg->appendChild($argText);
                }


            } else {
                fprintf(STDERR, "Unknown operator!\n");
                exit(23);
            }
        } elseif (checkForFourLabelSymSym($lineOfInstruction[0])) {
            $instructionOpCode = $doc->createAttribute("opcode");
            $instructionOpCode->value = $lineOfInstruction[0];
            $instruction->appendChild($instructionOpCode);

            //  <label> <symb> <symb>
            if (isOpLabel($lineOfInstruction[1]) && isOpSym($lineOfInstruction[2])) {
                $i = 1;
                $usingType = "label";
                $arg = $doc->createElement("arg".$i);
                $instruction->appendChild($arg);
                $type = $doc->createAttribute("type");
                $type->value = $usingType;
                $arg->appendChild($type);
                $argValue = "$lineOfInstruction[1]";
                $argText = $doc->createTextNode($argValue);
                $arg->appendChild($argText);
                $i++;

                $arg = $doc->createElement("arg".$i);
                $instruction->appendChild($arg);
                $type = $doc->createAttribute("type");
                $type->value = $symbType;
                $arg->appendChild($type);
                $argValue = "$symbValue";
                $argText = $doc->createTextNode($argValue);
                $arg->appendChild($argText);

                if (isOpSym($lineOfInstruction[3])) {
                    $i = 3;
                    $arg = $doc->createElement("arg".$i);
                    $instruction->appendChild($arg);
                    $type = $doc->createAttribute("type");
                    $type->value = $symbType;
                    $arg->appendChild($type);
                    $argValue = "$symbValue";
                    $argText = $doc->createTextNode($argValue);
                    $arg->appendChild($argText);
                }
            } else {
                fprintf(STDERR, "Unknown operator!\n");
                exit(23);
            }  
        } else {
            fprintf(STDERR, "Unknown operator!\n");
            exit(23);
        }
    } else {
        fprintf(STDERR, "Unknown operator!\n");
        exit(23);
    }

    $order++;
    $ccc++;
}

$programRoot = $doc->appendChild($programRoot);

echo $doc->saveXML();
exit(0);    // end of program

/**
 * @brief Control non-valid symbols
 * @param string	String for control
 * @return String with new symbols, if first-string have non-valid symbols
 */
function checkNevalidSymbols($string) {
    return str_replace(
        array("&", "<", ">", '"', "'"),
        array("&amp;", "&lt;", "&gt;", "&quot;", "&apos;"), 
        $string);
}

/**
 * @brief Function which control program instructions with 3 arguments: <instruction> <var> <symb>
 * @param opcode	Instruction for control
 * @return True - if the instruction is correct; False - if the instruction isn't correct
 */
function checkForThreeArgVarSymb($opcode) {
    $opcode = strtoupper($opcode);
    if (($opcode == "MOVE") ||
        ($opcode == "INT2CHAR") ||
        ($opcode == "STRLEN") ||
        ($opcode == "TYPE") ||
        ($opcode == "NOT")) {
            return true;
        } else {
            return false;
        }
}

/**
 * @brief Function which control program instructions with 4 arguments: <instruction> <label> <symb> <symb>
 * @param opcode	Instruction for control
 * @return True - if the instruction is correct; False - if the instruction isn't correct
 */
function checkForFourLabelSymSym($opcode) {
    $opcode = strtoupper($opcode);
    if (($opcode == "JUMPIFEQ") ||
        ($opcode == "JUMPIFNEQ")) {
            return true;
        } else {
            return false;
        }
}

/**
 * @brief Function which control program instructions with 4 arguments: <instruction> <var> <symb> <symb>
 * @param opcode	Instruction for control
 * @return True - if the instruction is correct; False - if the instruction isn't correct
 */
function checkForFourVarSymSym($opcode) {
    $opcode = strtoupper($opcode);
    if (($opcode == "ADD") ||
        ($opcode == "SUB") ||
        ($opcode == "MUL") ||
        ($opcode == "IDIV") ||
        ($opcode == "LT") ||
        ($opcode == "GT") ||
        ($opcode == "EQ") ||
        ($opcode == "AND") ||
        ($opcode == "OR") ||
        ($opcode == "STRI2INT") ||
        ($opcode == "CONCAT") ||
        ($opcode == "GETCHAR") ||
        ($opcode == "SETCHAR")) {
            return true;
        } else {
            return false;
        }
}

/**
 * @brief Control types
 * @param opcode	Type of argument
 * @return True - if the type is correct; False - if the type isn't correct
 */
function isOpType($opcode) {
    return (($opcode == "int") || ($opcode == "string") || ($opcode == "bool") || ($opcode == "nil"));
}

/**
 * @brief Function which control program instructions with 3 arguments: <instruction> <var> <type>
 * @param opcode	Instruction for control
 * @return True - if the instruction is correct; False - if the instruction isn't correct
 */
function checkForThreeArg($opcode) {
    $opcode = strtoupper($opcode);
    if ($opcode == "READ") {
        return true;
    } else {
        return false;
    }
}

/**
 * @brief Control label syntax
 * @param opcode	Label argument
 */
function isOpLabel($opcode) {
    return preg_match("/^[[:alpha:]_\-$&%*!?][[:alnum:]_\-$&%*!?]*$/", $opcode);
}

/**
 * @brief Function which control program instructions with 2 arguments: <instruction> <label>
 * @param opcode	Instruction for control
 * @return True - if the instruction is correct; False - if the instruction isn't correct
 */
function checkForTwoArgLabel($opcode) {
    $opcode = strtoupper($opcode);
    if (($opcode == "CALL") ||
        ($opcode == "LABEL") ||
        ($opcode == "JUMP")) {
            return true;
        } else {
            return false;
        }
}

/**
 * @brief Control symbols
 * @param opcode	Symbol-argument
 * @return True - if the symbol-type is correct, else exit with code 23
 */
function isOpSym($opcode) {
    global $symbValue;
    $checkLine = explode("@", $opcode, 2);  // cut string in @ 
    $lineCount = count($checkLine);
    // control count of elements
    if ($lineCount < 2) {
		fprintf(STDERR, "PARSER ERROR: Musí existovat znak @ v konstantní definici\n");
        exit(23);
    }
    // check all types

    //  type int
    if ($checkLine[0] == "int") {
        // control that int is not empty
        if ($checkLine[1] == "" || $checkLine[1] == "\n") {
            fprintf(STDERR, "PARSER ERROR: Typ int nemůže byt prazdný\n");
			exit(23);
        }
        if(!preg_match("/^[-+]?\d+$/", $checkLine[1])) {
            fprintf(STDERR, "PARSER ERROR: Neplatné znaky v constante int ('$checkLine[1]')\n");
			exit(23);
        }
        $symbValue = $checkLine[1];
    
    // type bool
    } elseif ($checkLine[0] == "bool") {
        if (($checkLine[1] != "true") && ($checkLine[1] != "false")) {
            fprintf(STDERR, "PARSER ERROR: Neplatné znaky v constante bool('$checkLine[1]')\n");
			exit(23);
        }
        $symbValue = $checkLine[1];
    
    // type string
    } elseif ($checkLine[0] == "string") {
        // if string is not empty
        if ($lineCount != "" || $lineCount != "\n") {
            if(preg_match("/(?!\\\\[0-9]{3})[[:blank:]\\\\#]/", $checkLine[1])) {
				global $order;
				fprintf(STDERR, "PARSER ERROR: Neplatné znaky v constante string (instrcution #$order)\n");
				exit(23);
			}
        }
        $symbValue = $checkLine[1];
        //$checkLine[1] = $opcode;

    
        // special type
    } elseif (($checkLine[0] == "LT") ||
              ($checkLine[0] == "TF") ||
              ($checkLine[0] == "GF")) {
                if(!preg_match("/^[[:alpha:]\_\-\$\&\%\*\!\?][[:alnum:]_\-\$\&\%\*\!\?]*$/", $checkLine[1])) {
                    global $order;
                    fprintf(STDERR, "PARSER ERROR: Neplatné znaky v var (instrcution #$order)\n");
				    exit(23);

                }				
                $checkLine[0] = "var";	// type var
                $symbValue = $opcode;

    // type nil
    } elseif ($checkLine[0] == "nil") {
        if ($checkLine[1] != "nil") {
            global $order;
            fprintf(STDERR, "PARSER ERROR: Neplatné znaky v var (instrcution #$order)\n");
			exit(23);
        }
        $symbValue = $checkLine[1];
    } else {
        global $order;
        fprintf(STDERR, "PARSER ERROR: Neplatné typ constanty ('$checkLine[0]' in instrcution #$order)\n");
		exit(23);
    }
    global $symbType;
    $symbType = $checkLine[0];
     
    //printf("$symbType\n");
    return true;
}

/**
 * @brief Function which control program instructions with 2 arguments: <instruction> <symb>
 * @param opcode	Instruction for control
 * @return True - if the instruction is correct; False - if the instruction isn't correct
 */
function checkForTwoArgSym($opcode) {
    $opcode = strtoupper($opcode);
    if (($opcode == "PUSHS") ||
        ($opcode == "WRITE") ||
        ($opcode == "EXIT") ||
        ($opcode == "DPRINT")) {
            return true;
        } else {
            return false;
        }
}

/**
 * @brief Control var-argument syntax
 * @param opcode	Var-argument for control
 */
function isOpVar($opcode) {
    return preg_match("/^(LF|TF|GF)@[[:alpha:]\_\-\$\&\%\*\!\?][[:alnum:]\_\-\$\&\%\*\!\?]*$/", $opcode);
}

/**
 * @brief Function which control program instructions with 2 arguments: <instruction> <var>
 * @param opcode	Instruction for control
 * @return True - if the instruction is correct; False - if the instruction isn't correct
 */
function checkForTwoVarArg($opcode) {
    $opcode = strtoupper($opcode);
    if (($opcode == "DEFVAR") ||
        ($opcode == "POPS")) {
            return true;
        } else {
            return false;
        }
}

/**
 * @brief Function which control program instructions with 1 arguments: <instruction>
 * @param opcode	Instruction for control
 * @return True - if the instruction is correct; False - if the instruction isn't correct
 */
function checkForOneArg($opcode) {
    $opcode = strtoupper($opcode);
    if (($opcode == "CREATEFRAME") || 
        ($opcode == "PUSHFRAME") ||
        ($opcode == "POPFRAME") || 
        ($opcode == "RETURN") ||
        ($opcode == "BREAK")) {
            return true;
        } else {
            return false;
        }
}

/**
 * @brief Function spliting string of commands on elements for control 
 * @param lineOfProgram	Line for splitting
 * @return Array with line elements
 */
function dividingLine($lineOfProgram) {
    //$lineOfProgram = preg_replace('!#.*?\n!', '', $lineOfProgram); // removes # comments
    $lineOfProgram = explode("#", $lineOfProgram, 2);
    $lineOfProgram = $lineOfProgram[0];
    $lineOfProgram = trim($lineOfProgram);
    checkNevalidSymbols($lineOfProgram);
    //echo("$lineOfProgram\n");
    // dividing line
    $divLineArray = preg_split("/[[:blank:]]+/", $lineOfProgram, 4, PREG_SPLIT_NO_EMPTY);
    return $divLineArray;
}

/**
 * @brief Reading and control arguments
 */
function controlArguments() {
    // Read arguments
    $arguments = array("help");
    global $argc;
    $usingArguments = getopt("", $arguments);
    
    if ($argc == 1) {
        return;
    } else if ($argc == 2) {
        // if we use --help
        if (array_key_exists('help', $usingArguments)) {
            fprintf(STDERR, "Tento skript načte zdrojový kód v IPPcode21 z standartního vstupu,\n");
            fprintf(STDERR, "zkontroluje lexikální a syntaktickou správnost a tiskne XML reprezentaci programu\n");
            fprintf(STDERR, "na standartní výstup\n");
            exit(0);
        } else {
            fprintf(STDERR, "Parametr --help nelze kombinovat s žádným dalším parametrem\n");
            exit(10);
        } 
    } else {
        fprintf(STDERR,"Chybějící parametr skriptu\n");
        exit(10);
    }
    
}