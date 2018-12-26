import xml.etree.ElementTree as Et
import time
aa = time.time()

tree = Et.parse('pl_p4_trz@route2.xml')
root = tree.getroot()

slownikPrzebiegow = {}


def pobieranie(klucze, typ):
    slownikPrzebiegow[klucze][typ] = {}
    uniq_number = 1
    for elementyPrzebiegu in root.findall("./Line/Module/Route/[@number='%s']/Parts/Part/[@type='%s']/RouteElems/"
                                          % (klucze, typ)):
        slownikPrzebiegow[klucze][typ][str(uniq_number)] = {}
        if elementyPrzebiegu.attrib['cmdName'] == 'NN':
            continue  # nie wpisujemy elementów o nazwie 'NN'
        else:
            slownikPrzebiegow[klucze][typ][str(uniq_number)]['Nazwa'] = elementyPrzebiegu.attrib['cmdName']
        slownikPrzebiegow[klucze][typ][str(uniq_number)]['Typ'] = elementyPrzebiegu.attrib['type']
        try:
            slownikPrzebiegow[klucze][typ][str(uniq_number)]['nazwaWspolnejIzolacji'] = (
                                                                elementyPrzebiegu.attrib['comInsName'])
            slownikPrzebiegow[klucze][typ][str(uniq_number)]['Plus'] = elementyPrzebiegu.attrib['plus']
            slownikPrzebiegow[klucze][typ][str(uniq_number)]['Polozenie'] = elementyPrzebiegu.attrib['position']
        except KeyError:
            pass

        for parametryElementow in elementyPrzebiegu:
            if parametryElementow.attrib['keyword'] == 'ILM_Usage_Case':
                slownikPrzebiegow[klucze][typ][str(uniq_number)]['UsageCase'] = parametryElementow.attrib['value']
            elif parametryElementow.attrib['keyword'] == 'Usage_Mark':
                slownikPrzebiegow[klucze][typ][str(uniq_number)]['UsageMark'] = parametryElementow.attrib['value']
            elif parametryElementow.attrib['keyword'] == 'Usage_Func':
                slownikPrzebiegow[klucze][typ][str(uniq_number)]['UsageFunc'] = parametryElementow.attrib['value']
            elif (slownikPrzebiegow[klucze][typ][str(uniq_number)]['Typ'] == 'LT'
                    and parametryElementow.attrib['keyword'] == 'Elem_Addp'):
                slownikPrzebiegow[klucze][typ][str(uniq_number)]['elemAddp'] = int(
                                                                                parametryElementow.attrib['value'], 16)

        if slownikPrzebiegow[klucze][typ][str(uniq_number)]['UsageCase'].endswith('00'):
            del slownikPrzebiegow[klucze][typ][str(uniq_number)]  # Usuwanie bezużytecznych elementów, UsageCase '00'.

        uniq_number += 1


for numeryPrzebiegow in root.iter('Route'):
    if numeryPrzebiegow.attrib['type'] == 'MR' or numeryPrzebiegow.attrib['type'] == 'SR':
        slownikPrzebiegow[numeryPrzebiegow.attrib['number']] = {'nazwa': numeryPrzebiegow.attrib['name']}
        listaWykluczen = []
        for wykluczeniaSpec in root.findall("./Line/Module/Route/[@number='%s']/IncRoutes/"
                                            % numeryPrzebiegow.attrib['number']):
            listaWykluczen.append((wykluczeniaSpec.attrib['rNumber'], wykluczeniaSpec.attrib['incType']))
        slownikPrzebiegow[numeryPrzebiegow.attrib['number']]['wyklSpec'] = listaWykluczen

for keys in slownikPrzebiegow.keys():
    slownikPrzebiegow[keys]['parametryPrzebiegu'] = {}
    for parametryPrzebiegu in root.findall("./Line/Module/Route/[@number='%s']/Params/" % keys):
        if parametryPrzebiegu.attrib['keyword'] == 'Overlap_Rel_Time':
            slownikPrzebiegow[keys]['parametryPrzebiegu']['OverlapRelTime'] = parametryPrzebiegu.attrib['value']
        elif parametryPrzebiegu.attrib['keyword'] == 'US_Aspect_to_Switch_on':
            slownikPrzebiegow[keys]['parametryPrzebiegu']['UsAspectToSwitchOn'] = parametryPrzebiegu.attrib['value']
        elif parametryPrzebiegu.attrib['keyword'] == 'Speed_Signal':
            slownikPrzebiegow[keys]['parametryPrzebiegu']['SpeedSignal'] = parametryPrzebiegu.attrib['value']
        elif parametryPrzebiegu.attrib['keyword'] == 'Limit_On_No_Proceed':
            slownikPrzebiegow[keys]['parametryPrzebiegu']['LimitOnNoProceed'] = parametryPrzebiegu.attrib['value']
        elif parametryPrzebiegu.attrib['keyword'] == 'Supervised_Dir_Indicator':
            slownikPrzebiegow[keys]['parametryPrzebiegu']['SupervisedDirIndicator'] = parametryPrzebiegu.attrib['value']
        elif parametryPrzebiegu.attrib['keyword'] == 'Not_Supervised_Indicator':
            slownikPrzebiegow[keys]['parametryPrzebiegu']['NotSupervisedIndicator'] = parametryPrzebiegu.attrib['value']

for keys in slownikPrzebiegow:
    for czesciPrzebiegu in ('MR', 'SR', 'FP', 'OL', 'FO'):
        pobieranie(keys, czesciPrzebiegu)

# TODO generacja wykluczeń


for numer in slownikPrzebiegow.keys():
    wykluczeniaZwyczajne = []
    for numer2 in slownikPrzebiegow.keys():
        for typ in ('MR', 'SR', 'FP', 'OL', 'FO'):
            for numerElementu in slownikPrzebiegow[numer][typ].keys():
                if slownikPrzebiegow[numer][typ][numerElementu]['UsageCase'] == 













# TODO zamiana nazw na rzeczywiste
# TODO excel formatka
# TODO podzial na arkusze
# TODO wpisywanie do arkuszy

#  print(slownikPrzebiegow['687'])
