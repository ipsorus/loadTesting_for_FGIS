from datetime import datetime, date, time, timedelta
import random
import os


#Количество заявок о поверках СИ
NUMBER_OF_XML = 25
#Количество записей о поверках СИ
NUMBER_OF_RESULT = 5000

path_for_files = os.getcwd()
path_for_files = path_for_files + '/' + str(NUMBER_OF_RESULT)
os.mkdir(path_for_files)

total_numbers_of_xml = 0 #Общее количество заявок
total_applicable = 0     #Общее количество пригодных СИ
total_inapplicable = 0   #Общее количество непригодных СИ

for n in range(NUMBER_OF_XML):
    #Условный шифр знака поверки
    signCipher_element = 'М'

    #Количество записей о поверках СИ
    NUMBER_OF_RESULT = NUMBER_OF_RESULT

    #Название файла
    name_of_file = r'loadTest_' + str(NUMBER_OF_RESULT) + '_' + str(n+1) + '_signCipher_' + signCipher_element + '.xml'

    FileFullPath = os.path.join(path_for_files, name_of_file)  #Путь сохранения файла

    Reestr_number = ['16078-05', '42453-09', '10158-85', '1002-55', '10337-86', '10135-15', '10088-85', '1009-56']

    TYPE_SI = {'16078-05': ['СХВ-15', 'СХВ-15Д', 'СХВ-20', 'СХВ-20Д', 'СГВ-15', 'СГВ-15Д', 'СГВ-20', 'СГВ-20Д'], '42453-09':['ВИТ-1', 'ВИТ-2', 'ВИТ-3'], '10158-85':'Электроника 21-06', '1002-55':'Д528', '10337-86':'Янтарь', '10135-15':'МП-У', '10088-85':'МТ-15М', '1009-56':'1СД'}

    applicable = 0
    inapplicable = 0
    numbers_of_items = 0

    with open (FileFullPath, 'w', encoding='utf-8') as sample:

        header_1 = '<?xml version="1.0" encoding="utf-8" ?>'
        header_2 = '<gost:application xmlns:gost="urn://fgis-arshin.gost.ru/module-verifications/import/2020-04-14">'
        header = header_1 + header_2
        sample.write(header)

    with open (FileFullPath, 'a', encoding='utf-8') as sample_body:

        for i in range(NUMBER_OF_RESULT):

            #Модификация СИ и Тип СИ
            mitypeNumber = Reestr_number[random.randint(0, len(Reestr_number)-1)]
            modification = TYPE_SI[mitypeNumber]

            if type(modification) is list:
                modification = modification[random.randint(0, len(modification) - 1)]

            certNum = str(random.randint(1, 500)) + str(random.randint(1, 500)) + str(i)                            #Номер свидетельства/извещения о непригодности СИ

            manufactureNum = str(NUMBER_OF_RESULT) + "-" + str(random.randint(1, 998)) + str(random.randint(0, i))  #Заводской номер СИ
            manufactureYear = random.randint(2005, 2020)                                                            #Дата производства СИ

            result_start = '<gost:result>'
            miInfo_start = '<gost:miInfo>'
            singleMI_start = '<gost:singleMI>'
            mitypeNumber = f'<gost:mitypeNumber>{mitypeNumber}</gost:mitypeNumber>'
            manufactureNum = f'<gost:manufactureNum>{manufactureNum}</gost:manufactureNum>'
            manufactureYear = f'<gost:manufactureYear>{manufactureYear}</gost:manufactureYear>'
            modification = f'<gost:modification>{modification}</gost:modification>'
            singleMI_close = '</gost:singleMI>'
            miInfo_close = '</gost:miInfo>'

            miInfo = miInfo_start + singleMI_start + mitypeNumber + manufactureNum + manufactureYear + modification + singleMI_close + miInfo_close

            verification_generator = random.uniform(0, 5)  #Генератор чисел с плавающей точкой для статуса поверки (пригодно, непригодно)

            MPI_interval = ['365', '730' , '1095']                          #МПИ: 1год, 2года, 3года
            MPI = int(MPI_interval[random.randint(0, 2)])

            vrfDay = random.randint(0, 45)                                  #Диапазон поверок 45 дней

            current_date = datetime.now() - timedelta(vrfDay)               #Текущая дата
            vrfDate = datetime.now() - timedelta(vrfDay)                    #Вычисление даты поверки в диапазоне 45 дней
            vrfDate = current_date.strftime('%Y-%m-%d')                     #Отформатированная дата поверки

            validDate = current_date - timedelta(1) + timedelta(days = MPI)
            validDate = validDate.strftime('%Y-%m-%d')                      #Отформатированная дата действия поверки


            if verification_generator >= 0.1:
                signCipher = f'<gost:signCipher>{signCipher_element}</gost:signCipher>'
                vrfDate = f'<gost:vrfDate>{vrfDate}+03:00</gost:vrfDate>'
                validDate = f'<gost:validDate>{validDate}+03:00</gost:validDate>'

                valid = signCipher + vrfDate + validDate

                signPass = random.randint(0, 1)                                                     #Знак поверки в паспорте
                if signPass == 0:
                    signPass = 'false'
                else:
                    signPass = 'true'

                signMi = random.randint(0, 1)                                                       #Знак поверки на СИ
                if signMi == 0:
                    signMi = 'false'
                else:
                    signMi = 'true'

                applicable_start = '<gost:applicable>'
                certNum = f'<gost:certNum>{certNum}</gost:certNum>'
                signPass = f'<gost:signPass>{signPass}</gost:signPass>'
                signMi = f'<gost:signMi>{signMi}</gost:signMi>'
                applicable_close = '</gost:applicable>'
                verification_res = applicable_start + certNum + signPass + signMi + applicable_close
                applicable += 1
            else:
                signCipher = f'<gost:signCipher>{signCipher_element}</gost:signCipher>'
                vrfDate = f'<gost:vrfDate>{vrfDate}+03:00</gost:vrfDate>'

                valid = signCipher + vrfDate

                inapplicable_start = '<gost:inapplicable>'
                noticeNum = f'<gost:noticeNum>{certNum}</gost:noticeNum>'
                inapplicable_close = '</gost:inapplicable>'
                verification_res = inapplicable_start + noticeNum + inapplicable_close
                inapplicable += 1


            docTitle = f'<gost:docTitle>МП 001-01-0001 "Тестовая методика"</gost:docTitle>'

            means_of_verification = random.randint(0, 4) #Выбор одного из 5-ти средств поверки

            means_start = '<gost:means>'

            npe = ''
            if means_of_verification == 0:
                npe_start = '<gost:npe>'
                npe_number_1 = '<gost:number>гэт1-2018</gost:number>'
                npe_close = '</gost:npe>'
                npe = npe_start + npe_number_1 + npe_close

            uve = ''
            if means_of_verification == 1:
                uve_start = '<gost:uve>'
                uve_number_1 = '<gost:number>2.1.ZAM.0001.2012</gost:number>'
                uve_close = '</gost:uve>'
                uve = uve_start + uve_number_1 + uve_close

            ses = ''
            if means_of_verification == 2:
                ses_start = '<gost:ses>'
                se_start = '<gost:se>'
                typeNum = '<gost:typeNum>ГСО 1002-76</gost:typeNum>'
                ses_manufactureYear = '<gost:manufactureYear>2020</gost:manufactureYear>'
                ses_manufactureNum = '<gost:manufactureNum>65656</gost:manufactureNum>'
                se_close = '</gost:se>'
                ses_close = '</gost:ses>'
                ses = ses_start + se_start + typeNum + ses_manufactureYear + ses_manufactureNum + se_close + ses_close

            mieta = ''
            if means_of_verification == 3:
                mieta_start = '<gost:mieta>'
                mieta_number = '<gost:number>20189.07.РЭ.01351</gost:number>'
                mieta_close = '</gost:mieta>'
                mieta = mieta_start + mieta_number + mieta_close

            mis = ''
            if means_of_verification == 4:
                mis_start =	'<gost:mis>'
                mi_start = '<gost:mi>'
                typeNum = '<gost:typeNum>100-49</gost:typeNum>'
                mieta_manufactureNum = '<gost:manufactureNum>32312313</gost:manufactureNum>'
                mi_close = '</gost:mi>'
                mis_close =	'</gost:mis>'
                mieta = mis_start + mi_start + typeNum + mieta_manufactureNum + mi_close + mis_close

            means_close = '</gost:means>'

            additional_info_list = ['<gost:ranges>В полном объеме</gost:ranges>', '<gost:values>В полном объеме</gost:values>', '<gost:channels>В полном объеме</gost:channels>', '<gost:blocks>Отдельные автономные блоки</gost:blocks>']
            additional_info = additional_info_list[random.randint(0, 3)]

            result_close = '</gost:result>'


            body = result_start + miInfo + valid + verification_res + docTitle + means_start + npe + uve + ses + mieta + mis + means_close + additional_info + result_close
            sample_body.write(body)


            numbers_of_items += 1

    with open (FileFullPath, 'a', encoding='utf-8') as sample:
        footer = '</gost:application>'
        sample.write(footer)

    total_numbers_of_xml += 1
    total_applicable += applicable
    total_inapplicable += inapplicable

file_info = 'file_' + str(NUMBER_OF_RESULT) + '.txt'
FileFullPathInfo = os.path.join(path_for_files, file_info)  #Путь сохранения инфо-файла

with open (FileFullPathInfo, 'w', encoding='utf-8') as txt:

    str_1 = f'Количество заявок = {total_numbers_of_xml}'
    str_2 = f'Записей в каждой заявке = {numbers_of_items}'
    str_3 = f'Пригодные СИ: {total_applicable}, Непригодные СИ: {total_inapplicable}'

    info_file = str_1 + '\n' + str_2 + '\n' + str_3
    txt.write(info_file)

print('Формирование файлов завершено!')
print(f'Количество заявок = {total_numbers_of_xml}')
print(f'Записей в каждой заявке = {numbers_of_items}')
print(f'Пригодные СИ: {total_applicable}, Непригодные СИ: {total_inapplicable}')