import tkinter as tk
from tkinter import ttk
import json


def load_available_ids(filepath):
    ids = []
    try:
        with open(filepath, 'r') as file:
            data = file.read().strip()
            if data:
                ids = [int(id) for id in data.split()]
    except FileNotFoundError:
        ids = []
    return ids

def find_smallest_missing_id(ids):
    for i in range(1000):
        if i not in ids:
            return i
    return None  # Trường hợp tất cả các ID từ 0 đến 999 đều đã có

def add_id_to_file(new_id, filepath):
    try:
        with open(filepath, 'r') as file:
            data = file.read().strip()
            if data:
                ids = [int(id) for id in data.split()]
            else:
                ids = []
    except FileNotFoundError:
        ids = []

    if new_id not in ids:
        ids.append(new_id)
        ids.sort()

        with open(filepath, 'w') as file:
            file.write(' '.join(map(str, ids)))

def delete_id_from_file(id_to_delete, filepath):
    # Đọc các ID từ file
    ids = load_available_ids(filepath)
    # Loại bỏ ID cần xóa nếu có
    if id_to_delete in ids:
        ids.remove(id_to_delete)

    # Ghi lại các ID còn lại vào file
    with open(filepath, 'w') as file:
        file.write(' '.join(map(str, ids)))

def is_username_unique(username):
    data = load_data_json('accounts.json')
    usernames = [account["username"] for account in data]
    return username not in usernames

def load_data_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return []

def save_data_json(filename, data):
    try:
        with open(filename, 'r') as file:
            user_details = json.load(file)
    except FileNotFoundError:
        user_details = []
    user_details.append(data)

    with open(filename, 'w') as file:
        json.dump(user_details, file, indent=4)

def save_data_login(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
def save_member_info_login(filename, new_member_info):
#Khong dung
    data = load_data_json(filename)
    data.append(new_member_info)
    save_data_login(filename, data)