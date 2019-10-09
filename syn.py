#!/usr/bin/python


################
##  XVASKO14  ##
################




import sys, os, codecs, re, pprint


#urcim si globalne premene
# prve INPUT
NastavInp = False
#OUTPUT
NastavOut = False
# dalsiu pre FORMAT
NastavFormat = False
# a taktiez BR
NastavBr = False

SubInp = sys.stdin
SubOut = sys.stdout
SubFormat = ""

StrInp = ""
StrFormat = ""

#klasicky vypis HELP
def vypis_help():
    print("AUTOR : MICHAL VASKO \n\
           LOGIN : xvasko14\n\
           -------------------------\n\
           --help vypise napovedu\n\
           --input=subor\n\
           --output=subor\n\
           --format=subor\n\
           --br : za kazdy riadok dat <br/>\n\
           ---------------------------------\n\
           ")
    exit(0)
    



#funckia kde sa riesia parametre 
#pouzil som re.match 
def Argumenty(argums):
    # urcim si vstky potrebne premene ktore budem potrebovat
    del argums[0]
    pocitadlo=0
    z=0
    result=""
    table = {'input':'','input_on':0,'output':'','output_on':0,'format':'','br':0}

    for arguments in argums:
        # prvy pre argument HELP
        if (len(argums)==1 and arguments=="--help"):
            vypis_help()
            exit (0)

        else :
            # dalej riesime vstupny subor
            if (re.match('--input=.*',arguments)):
                global NastavInp
                global SubInp

                if(NastavInp):
                    print("Zle ste zadali argumenty",file=sys.stderr)
                    sys.exit(1)

                NastavInp = True

                try:
                    SubInp = codecs.open(sys.argv[z][8:], 'r', 'utf-8')
                except:
                    print("Subor sa neda otvorit alebo neexistuje",file=sys.stderr)
                    sys.exit(2)

                result = re.match('--input=(.*)',arguments)
                table['input']=result.group(1)
                pocitadlo+=1

            # vystupny subor
            if (re.match('--output=[^ ]+',arguments)):
                global NastavOut
                global SubOut

                if(NastavOut):
                    print("Zle ste zadali argumenty",file=sys.stderr)
                    sys.exit(1)

                NastavOut = True

                try:
                    SubOut = codecs.open(sys.argv[z][9:], 'w', 'utf-8')
                except:
                    print("Problem so vstupnym suborom,nejde otvorit/vytvorit",file=sys.stderr)
                    sys.exit(3)
                result = re.match('--output=(.*)',arguments)
                table['output']=result.group(1)
                table['output_on']=1
                pocitadlo+=1
            # tu si nacitam formatovaci subor
            if (re.match('--format=.*',arguments)):
                global NastavFormat
                global SubFormat

                if(NastavFormat):
                    print("Zle ste zadali argumenty",file=sys.stderr)
                    sys.exit(1)

                NastavFormat = True
                try:
                    SubFormat = codecs.open(sys.argv[z][9:], 'r', 'utf-8')
                except:
                    StrFormat = 0

                result = re.match('--format=(.*)',arguments)
                table['format']=result.group(1)
                pocitadlo+=1
            # a taktie moznost prepinaca BR , ktory tlaci za riadkom
            if (re.match('--br',arguments)):
                global NastavBr

                if(NastavBr):
                    print("Zle ste zadali argumenty",file=sys.stderr)
                    sys.exit(1)

                NastavBr = True
                pocitadlo+=1
        z += 1
    # v pripade ze nie su argumenty ok, riesime to chybou
    if (len(argums)!=pocitadlo):
        print("Zle ste zadali argumenty",file=sys.stderr)
        sys.exit(1)

    return table

# Funkcia ktora sa stara o formatovaci subor ktory spracuvava, 
def TabulkaFormatu():
    global StrFormat
    formatovaciaTabulka = []

    for line in StrFormat.splitlines():
        znacka = []
        split = line.split('\t', 1)
        try:
            znacka.append(split[0].strip())
            znacka.append(split[-1].strip())
        except:
            # vyskytla sa chyba vypisem co sa stalo a navrat(4)
            print("Chybny format vsetupneho suboru",file=sys.stderr)
            sys.exit(4)
        formatovaciaTabulka.append(znacka)
    return formatovaciaTabulka

# Touto funkciou riesime HTML znackovanie pddla regexch vyrazov
# Vsetko sa to riesi pomocou pola miesto
# Kde sa vkladaju prislusne znacky
def PoziciaZnac(formatovaciaTabulka):
    global StrInp
    miesto = [''] * (len(StrInp) + 1)
    for line in formatovaciaTabulka:
        PythReg = prevodRegex(line[0])
        for find in re.finditer(PythReg, StrInp, re.DOTALL):
            if(find.end() != find.start()):
                miesto[find.start()] = miesto[find.start()] + ZnackyHTML(line[1], True)
                miesto[find.end()] = ZnackyHTML(line[1], False) + miesto[find.end()]
    return miesto

# funkcia ktorou zaobstaravame to aby regexm vyrazom rozumel aj python 3 a preto ich prevadzame zo syn regexu na python regex
def prevodRegex(regex):
    PythReg = ''
    ZnakKoniec = ""
    negacia = ""

    # cyklus aby sme mohli prechadzat zaradom
    for znak in regex: 

        if znak == "%": 
            if ZnakKoniec == "%": 
                PythReg += "[" + "%" + "]" 
                ZnakKoniec = ""
                negacia = ""
            else:
                ZnakKoniec = znak 
        # riesenie pre libovolne znaky
        elif znak == "a":
            if ZnakKoniec == "%":
                if negacia == "":
                    PythReg += "."
                    ZnakKoniec = ""
                    negacia = ""
                else:
                    PythReg += "(3\[\]\!\@\#\\%\^\^\&\*\(\)4)"
                    ZnakKoniec = ""
                    negacia = ""
            else:
                PythReg += "[" + negacia + znak + "]"
                ZnakKoniec = znak
                negacia = ""

        elif znak == "!":
            if ZnakKoniec == "%":
                PythReg += negacia + "!"
                ZnakKoniec = ""
                negacia = ""
            else:
                negacia = "^"
                ZnakKoniec = znak

        elif znak == ".":
            if ZnakKoniec == "%":
                PythReg += negacia + "\."
                ZnakKoniec = ""
                negacia = ""
            else:
                ZnakKoniec = znak

        #pre znaky ako pismena cisla atd
        # pre cisla od 0 d 9
        elif znak == "d":
            if ZnakKoniec == "%":
                PythReg += "[" + negacia + "0-9" + "]"
                ZnakKoniec = ""
                negacia = ""
            else:
                PythReg += "[" + negacia + znak + "]"
                ZnakKoniec = znak
                negacia = ""
        # mala pismena
        elif znak == "l":
            if ZnakKoniec == "%":
                PythReg += "[" + negacia + "a-z" + "]"
                ZnakKoniec = ""
                negacia = ""
            else:
                PythReg += "[" + negacia + znak + "]"
                ZnakKoniec = znak
                negacia = ""
        #velka pismena
        elif znak == "L":
            if ZnakKoniec == "%":
                PythReg += "[" + negacia + "A-Z" + "]"
                ZnakKoniec = ""
                negacia = ""
            else:
                PythReg += "[" + negacia + znak + "]"
                ZnakKoniec = znak
                negacia = ""
        #male aj velke pismena
        elif znak == "w":
            if ZnakKoniec == "%":
                PythReg += "[" + negacia + "a-zA-Z" + "]"
                ZnakKoniec = ""
                negacia = ""
            else:
                PythReg += "[" + negacia + znak + "]"
                ZnakKoniec = znak
                negacia = ""
        #vsetky velke pismena a cisla
        elif znak == "W":
            if ZnakKoniec == "%":
                PythReg += "[" + negacia + "a-zA-Z0-9_" + "]"
                ZnakKoniec = ""
                negacia = ""
            else:
                PythReg += "[" + negacia + znak + "]"
                ZnakKoniec = znak
                negacia = ""


        #Specialne znaky, pri ktorych sa rozhodujem ci ich exsapujem, alebo proste to budu specialne python znaky
        elif znak == "|" or znak == "+" or znak == "(" or znak == ")" or znak == "*":
            if ZnakKoniec == "%":
                PythReg += "[" + negacia + "\\" + znak + "]"
                ZnakKoniec = ""
                negacia = ""
            else:
                PythReg += negacia + znak
                ZnakKoniec = znak
                negacia = ""


        #Biele znaky
        #znak tabulatoru alebo pre n- znak noveho riadku
        elif znak == "t" or znak == "n":
            if ZnakKoniec == "%":
                PythReg += "[" + negacia + "\\" +znak + "]"
                ZnakKoniec = ""
                negacia = ""
            else:
                PythReg += "[" + negacia + znak + "]"
                ZnakKoniec = znak
                negacia = ""

        elif znak == "s":
            if ZnakKoniec == "%":
                PythReg += "[" + negacia + " \t\n\r\f\v" + "]"
                ZnakKoniec = ""
                negacia = ""
            else:
                PythReg += "[" + negacia + znak + "]"
                ZnakKoniec = znak
                negacia = ""

        #par veci ktroe musiem vynechat
        elif znak == "[" or znak == "]" or znak == "{" or znak == "}" or znak == "$" or znak == "?" or znak == "\\" or znak == "^":
            PythReg += "[" + negacia + "\\" + znak + "]"
            ZnakKoniec = znak
            negacia = ""

        # ak nieco ine tak to skace do else
        else:
            if ZnakKoniec == "%":
                print("Regex nevalidny  " + regex, file = sys.stderr)
                exit(4)
            else:
                PythReg += "[" + negacia + znak + "]"
                ZnakKoniec = znak
                negacia = ""

    #Ak su tieto posledne, tak ich este pridam, lebo inak sa nenageneruju ale aj tak bude dalej chyba pri kontrole regexu
    if ZnakKoniec == "%" or ZnakKoniec == "!":
        PythReg += "\\"


    # treba sa postarat o osetrenie vselijakych chyb ktore mozu nastat
    #ked nastane cyba s bodkou
    if re.match(".*(([^%]|^)([%][%])*)\.\..*", regex) or re.match("^\..*", regex) or re.match(".*(([^%]|^)([%][%])*)\.$", regex):
        print("Zly regex  . " + regex, file = sys.stderr)
        exit(4)
    #mozne komplikacie zo zatvorkami
    if re.match(".*(([^%]|^)([%][%])*)\(\).*", regex):
        print("Zly regex  () " + regex, file = sys.stderr)
        exit(4)
    #zyslitka
    if re.match(".*(([^%]|^)([%][%])*)\|$", regex) or re.match("^\|.*", regex) or re.match(".*(([^%]|^)([%][%])*)\|\|.*", regex):
        print("Zly regex  | " + regex, file = sys.stderr)
        exit(4)
    #problemy s negaciou
    if re.match(".*(([^%]|^)([%][%])*)!\..*", regex) or re.match(".*(([^%]|^)([%][%])*)!\|.*", regex) or re.match(".*(([^%]|^)([%][%])*)!\*.*", regex) or re.match(".*(([^%]|^)([%][%])*)!!.*", regex) or re.match(".*(([^%]|^)([%][%])*)!\+.*", regex):
        print("Zly regex  ! " + regex, file = sys.stderr)
        exit(4)
    #vselijake dalsie...
    if re.match(".*(([^%]|^)([%][%])*)\|\..*", regex) or re.match(".*(([^%]|^)([%][%])*)\.\|.*", regex) or re.match("^\+.*", regex) or re.match("^\*.*", regex) or re.match(".*(([^%]|^)([%][%])*)\.\*.*", regex) or re.match(".*(([^%]|^)([%][%])*)\.\+.*", regex):
        print("Zly regex  | " + regex, file = sys.stderr)
        exit(4)

    #zistenie ci je vsetko v poriadku
    try:
        re.compile(PythReg)
    except re.error:
        print("Regex nevalidny  " + regex, file = sys.stderr)
        exit(4)
    return PythReg

# v tejto funkciu uz len kotrolujem ci je format v poriadku
def ForKontrola(formatovaciaTabulka):
    for line in formatovaciaTabulka:
        ZnackyHTML(line[1], True)
    return formatovaciaTabulka

# V tejto funkcii ziskame HTML znacky na zaklade retazca 
def ZnackyHTML(formatLine, start):
    HtmlZ = ''
    for format in formatLine.split(','):
        format = format.strip()
        znacka = '<'

        if(start == False):
            znacka += '/'

        #tucny text
        if(format == 'bold'):
            znacka += 'b'
        #text teletype
        elif(format == 'teletype'):
            znacka += 'tt'
        #podtrhnutie
        elif(format == 'underline'):
            znacka += 'u'
        #kurziva
        elif(format == 'italic'):
            znacka += 'i'
        #farba textu
        elif(re.match('color:[0-9a-fA-F]{6}', format)):
            znacka += 'font'
            if(start):
                znacka += ' color=#' + format[6:]
        #velkost text
        elif(re.match('size:[1-7]', format)):
            znacka += 'font'
            if(start):
                znacka += ' size=' + format[5:]
        # v pripade nevykoannia hornych veci skacime do chyboveho stavu
        else:
            print("Chybny format vsetupneho suboru",file=sys.stderr)
            sys.exit(4)
        znacka += '>'

        if(start):
            HtmlZ += znacka
        else:
            HtmlZ = znacka + HtmlZ

    return HtmlZ

# Dostavme vystup ked ulozime html znacky z miesta na urcenu poziciu
def Vystup(miesto):
    global StrInp
    String = ''
    for i in range(len(StrInp)):
        String += miesto[i] + StrInp[i]
    String += miesto[len(StrInp)]
    return String


# Hlavní tělo programu
#spracujem argumenty
argums = sys.argv
table = Argumenty(argums)

StrInp = SubInp.read()

#format
if(NastavFormat):
    if(StrFormat == 0):
        outputStr = StrInp
        NastavFormat = False
    else:
        StrFormat = SubFormat.read()
        if(len(StrFormat) == 0):
            outputStr = StrInp
            NastavFormat = False

else:
    outputStr = StrInp
#spracovanie formatu aby spravne pracovla a volanie funkciu
if(NastavFormat):
    formatovaciaTabulka = ForKontrola(TabulkaFormatu())
    miesto = PoziciaZnac(formatovaciaTabulka)
    outputStr = Vystup(miesto)

# ak nastane Br
if(NastavBr):
    outputStr = outputStr.replace("\n", "<br />\n")

SubOut.write(outputStr)

