# Chess Data Extractor v1.0
# Made by: Barnabás Horváth
# Date: 2019.05.23
#---------------------------------------------------- HASZNÁLAT --------------------------------------------------------------------
# Futáshoz szükséges: Python 3 telepítve az operációs rendszerre
# Futtatás módja: cmd-ben (parancssor) bemegyünk a mappába ahol a script van, majd kiadjuk a következő parancsot: python main.py
# Elindítjuk a scriptet, majd az első menüből kiválasztjuk hogy URL [1] vagy ID [2] alapján szeretnénk-e letölteni. Ennek megfelelően beírunk a terminálba egy 1-est vagy 2-est, majd entert 
# nyomunk. Előjön a 2. menü, ahol azt választjuk ki, hogy kézzel [1] vagy fileból [2] visszük be az adatokat. Ismét beírjuk a megfelelő számot, majd enter. Ha kézzel visszük be,
# akkor az 1. menüben választottak alapján vagy URL-eket, vagy ID-kat gépelünk be, vessző karakterrel elválasztva egymástól, szóköz nélkül. Ha fileból való bevitelt választottunk,
# először meg kell adnunk annak a MAPPÁNAK az elérési útját, ahol a fileunk található, majd enter, ezt követően pedig a file nevét KITERJESZTÉSSEL! együtt. A fileunknak mind ID mind URL
# esetén úgy kell kinéznie, hogy soronként tartalmaz egy ID-t / URL-t, majd sorvég karaktert (azaz minden adat után legyen enter nyomva, legyene mindegyik új sorban). 
# Ezt követően meg is vagyunk a bevitellel, csak várni kell amíg a script elvégzi a munkáját és kinyeri nekünk a szükséges adatokat. Ezeket egyrészt kiírja a képernyőre, másrészt
# kiírja egy "eredmenyek.txt" nevű fileba, amely file UGYANABBAN A MAPPÁBAN VAN MINT AHOL A BEVITELI FILEUNK ha volt ilyen, kézzel való begépelés esetén pedig 
# ABBAN A MAPPÁBAN LESZ AHONNAN A SCRIPT FUT.
# Megjegyzés: A program "szemetel", mivel nem törli a letöltött html fileokat, ezeket nekünk kell törölni ha meg akarunk tőlük szabadulni, egy chess_download nevű mappában lesznek, 
# az eredmenyek.txt-vel egy helyen.

#-----------------------------------------------------------------------------------------------------------------------------------
# Ismert problémák:
#   - Ha a játékos 0 GMS számmal rendelkezik, abból formázási probléma adódhat, a nevének hosszúságától függően

#-----------------------------------------------------------------------------------------------------------------------------------
# Necessary imports
import urllib.request
import os

# Function list --------------------------------------------------------------------------------------------------------------------

def getMethod():
    identification_method = 0

    while identification_method != '1' and identification_method != '2':
        print('URL vagy ID alapján szeretne letölteni?')
        print('[1] URL')
        print('[2] ID')
        identification_method = input()
        os.system('cls' if os.name == 'nt' else 'clear')
        if identification_method != '1' and identification_method != '2':
            print('[-] Invalid metódust adott meg! Kérem adja meg újra.')
    return identification_method


def inputMethod():
    input_method = 0

    while input_method != '1' and input_method != '2':
        print('Kézzel fogja beírni az adatokat vagy egy filet használ, ami a listát tartalmazza?')
        print('[1] Kézzel gépelem be')
        print('[2] File-t adok meg ami az adatokat tartalmazza')
        input_method = input()
        os.system('cls' if os.name == 'nt' else 'clear')
        if input_method != '1' and input_method != '2':
            print('[-] Invalid input metódust adott meg! Kérem adja meg újra.')
    return input_method

# Beveszi a html dokumentum nevét, visszaad egy listát, hogy: név, RTNG, GMS, RTNGúj-RTNGrégi
def getPlayerData(file_name):

    results = []
    valid = 1
    comma_in_name = 0
    html_file = open(file_name, 'r')
    file_string = html_file.read()


    if file_string.find('No data') != -1:
        valid = 0


    fs3_loc = file_string.find('font size=3') + 15 # This to get position of the name
    file_string = file_string[fs3_loc:]
    
    name_slice = file_string[:50]
    if name_slice.find(',') != -1:
        comma_in_name = 1
    name_end_loc = name_slice.find('(') - 1
    name = name_slice[:name_end_loc]
    namelength = len(name)
    if valid == 1:
        results.append(name)
    else:
        results.append('invalid játékos')
    # ------

    w40_1_loc = file_string.find('width=40') + 27 # This to get position of the RTNG number
    file_string = file_string[w40_1_loc:]

    RTNG_slice = file_string[:20]
    RTNG_end_loc = RTNG_slice.find('&')
    RTNG = RTNG_slice[:RTNG_end_loc]
    if valid == 1:
        results.append(RTNG)
    else:
        results.append('invalid játékos')
    # -----
    
    w30_1_loc = file_string.find('width=30') + 27 # This to get position of the GMS number
    file_string = file_string[w30_1_loc:]

    GMS_slice = file_string[:10] 
    GMS_end_loc = GMS_slice.find('&')
    GMS = GMS_slice[:GMS_end_loc]
    if valid == 1:
        results.append(GMS)
    else:
        results.append('invalid játékos')
    # -----

    w75_1_loc = file_string.find("width=75")
    file_string = file_string[w75_1_loc:]

    w40_2_loc = file_string.find("width=40") + 27
    file_string = file_string[w40_2_loc:]

    RTNG_2_slice = file_string[:20]
    RTNG_2_end_loc = file_string.find('&')
    RTNG_2 = RTNG_2_slice[:RTNG_2_end_loc]

    try:
        if valid == 1:
            results.append(str(int(RTNG)-int(RTNG_2)))
        else:
            results.append('invalid játékos')
    except ValueError:
        results.append('invalid játékos')

    return [results, namelength, comma_in_name]


# Main -----------------------------------------------------------------------------------------------------------------------------

os.system('cls' if os.name == 'nt' else 'clear')

id_method = getMethod()

input_method = inputMethod()

# download document(s) function: -------------------------------------------------

if input_method == '1':
    if id_method == '1':
        print('Adja meg az URL-(oka)t ilyen formátumban: https://ratings.fide.com/id.phtml?event=785857')
        print('Ha több URL-t is megad, válassza el őket a "," azaz "vessző" karakterrel, szóközök nélkül. A bevitel végén nyomjon ENTER-t. Az utolsó URL után nem kell vessző.')
        url = input()
        url_list = url.split(",")
    else:
        print('Adja meg az ID-(ke)t az URL végéről! (Pl.: 785857)')
        print('Ha több ID-t is megad, válassza el őket "," azaz "vessző" karakterrel, szóköz nélkül. Pl.: 12345,12289,11346')
        sakkid = input()
        sakkid_list = sakkid.split(',')
        url_list = []
        for element in sakkid_list:
            str_to_append_with = 'https://ratings.fide.com/id.phtml?event=' + element
            url_list.append(str_to_append_with)
else:
    while True:
        try:
            print('Adja meg a mappa elérési útját, amiben a file található! Pl.: C:\\Users\\Admin\\Documents')
            file_path = input()
            os.chdir(file_path)
            break
        except FileNotFoundError:
            print('Hibás a megadott mappa, adja meg újra.')

    while True:
        try:
            print('Adja meg az adatokat tartalmazó file nevét! Pl.: adatok.txt')
            file_name = input()
            file_list_in_directory = os.listdir()
            file_index_in_directory = file_list_in_directory.index(file_name)
            break
        except ValueError:
            print('Hibás a megadott file név, vagy a file nem létezik. Adja meg újra!')
    
    url_list = []

    f = open(file_name, "r")

    for line in f:
        if id_method == '1':
            line = line.rstrip()
            url_list.append(line)
        else:
            str_to_append_with = 'https://ratings.fide.com/id.phtml?event=' + line
            str_to_append_with = str_to_append_with.rstrip()
            url_list.append(str_to_append_with)
    f.close()





print('[+] HTML dokumentum(ok) letöltése ...')

try:
    os.mkdir("./chess_downloaded")
except FileExistsError:
    pass

os.system('cls' if os.name == 'nt' else 'clear')
file_num = 0
for url in url_list:
    file_path = './chess_downloaded/downloaded' + str(file_num) + '.html'
    print('[+] Letötés alatt: ' + url)
    urllib.request.urlretrieve(url, file_path)
    file_num += 1


os.chdir('./chess_downloaded')
result_list = []
namelen_list = []
comma_list = []
for i in range(0, file_num):
    player_data = getPlayerData('downloaded' + str(i) + '.html')
    result_list.append(player_data[0])
    namelen_list.append(player_data[1])
    comma_list.append(player_data[2])

os.chdir('./..')
if os.path.isfile("eredmenyek.txt"):
  os.remove("eredmenyek.txt")

result_file = open('eredmenyek.txt', 'a')
result_file.write('Név\t\t\t\tRTNG\t\tGMS\t\tRTNG különbség\n')
result_file.write('------------------------------------------------------------------------------------------------------------------------------------------------\n\n')
iterator = 0
for element in namelen_list:
    element = element // 8
    namelen_list[iterator] = element
    iterator += 1

os.system('cls' if os.name == 'nt' else 'clear')
print('\n------------------------------- EREDMÉNYEK -----------------------------\n')
print('Név\t\t\t\tRTNG\t\tGMS\t\tRTNG különbség\n')
print('--------------------------------------------------------------------------\n')
iterator = 0
for line in result_list:
    result_string = ",".join(line)

    if comma_list[iterator] == 1:
        comma_loc = result_string.find(',')
        new_result_string = result_string[:comma_loc] + result_string[comma_loc+1:]
    else:
        new_result_string = result_string

    comma_loc = new_result_string.find(',')
    tabs = ""
    tabnum = 4-namelen_list[iterator]
    for l in range(0, tabnum):
        tabs += '\t'
    iterator += 1
    newer_result_string = new_result_string[:comma_loc] + tabs + new_result_string[comma_loc+1:]

    newest_result_string = newer_result_string.replace(',', '\t\t')
    result_file.write(newest_result_string + '\n')
    print(newest_result_string)
result_file.close()
print('\n\n[+] Az eredmények az eredmenyek.txt fileba is el lettek mentve, ami a ' + os.getcwd() + ' helyen található')

