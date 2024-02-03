import xlrd
import re
import json
import yaml

def take_config(name):
    with open('config.yaml', 'r') as f:
        templates = yaml.safe_load(f)
        return templates[name]

def check_file(file_name, user_id):

    user_id = take_config(user_id)
    workbook = xlrd.open_workbook(file_name)
    sheet = workbook.sheet_by_index(0)

    data = []

    for rx in range(1, sheet.nrows - 1):
        row_dict = {}

        if user_id in sheet.cell_value(rx, 7):
            if 'прос.' in sheet.cell_value(rx, 13):
                row_dict['time_left'] = f"<b>Просрочка:</b> {sheet.cell_value(rx, 13)}"
            else:
                continue

            if sheet.cell_value(rx, 5) not in IGNORE_BUYERS:
                row_dict['buyer'] = f"<b>Юр. Лицо:</b> {sheet.cell_value(rx, 5)}"
            else:
                continue

            row_dict['adress'] = f"<b>Адрес: </b> {sheet.cell_value(rx, 2)}"

            document_data = re.search(r"(\d{7}) от (\d{2}\.\d{2}\.\d{4})", sheet.cell_value(rx, 6))
            row_dict['document'] = f"<b>Накладная:</b> {document_data.group(1)} от {document_data.group(2)}"
            
            row_dict['seller'] = f"<b>ТП:</b> {sheet.cell_value(rx, 7)}"
            row_dict['price'] = f"<b>Сумма:</b> {str(sheet.cell_value(rx, 10))} грн"
            row_dict['payed'] = f"<b>Оплачено;</b> {str(sheet.cell_value(rx, 11))} грн"
            row_dict['left'] = f"<b>Недоплата:</b> {str(sheet.cell_value(rx, 12))} грн"

            if not any(comment in sheet.cell_value(rx, 8) for comment in IGNORE_COMMENTS):
                row_dict['comment'] = f"<b>Комментарий:</b> {sheet.cell_value(rx, 8)}"
            else:
                continue

            data.append(row_dict)

    save_json(data)

def save_json(data):
    with open('files/data.json', "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

def debet_len():
    with open('files/data.json', "r") as json_file:
        return len(json.load(json_file))
    
def open_json():
    with open('files/data.json', "r") as json_file:
        json_data = json.load(json_file)
        return json_data
    
def create_answer():
    debet = debet_len()

    data = open_json()

    msg = []

    header = f"Количество долгов: {debet}\nНа данный момент существуют такие долги: \n\n"

    msg.append(header)

    for clients in data:
        client_list = ''
        client_list += "\n" + "_" * 35 + "\n\n"
        for value in clients:
            client_list += f"{clients[value]}\n"
        client_list += "\n" + "_" * 35 + "\n\n"
        msg.append(client_list)
    return msg

IGNORE_BUYERS = take_config("IGNORE_BUYERS")
IGNORE_COMMENTS = take_config("IGNORE_COMMENTS")
