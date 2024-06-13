import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import file_method
from datetime import datetime

import frm_admin

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login form")
        self.root.geometry("800x600")

        tk.Label(root, text="Username").grid(row=0, column=0)
        self.entry_user_name = tk.Entry(root)
        self.entry_user_name.grid(row=0, column=1)

        tk.Label(root, text="Password").grid(row=1, column=0)
        self.entry_password = tk.Entry(root, show='*')
        self.entry_password.grid(row=1, column=1)

        tk.Button(root, text="Tạo tài khoản", command=self.create_account_window).grid(row=2, column=0)
        tk.Button(root, text="Login", command=self.login).grid(row=2, column=1, padx=3)

    def create_account_window(self):
        create_window = tk.Toplevel(self.root)
        create_window.title("Tạo tài khoản")
        create_window.geometry("300x300")

        tk.Label(create_window, text="Tên đăng nhập:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_username = tk.Entry(create_window)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(create_window, text="Mật khẩu:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_password_new = tk.Entry(create_window, show='*')
        self.entry_password_new.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(create_window, text="Nhập lại mật khẩu:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_password_confirm = tk.Entry(create_window, show='*')
        self.entry_password_confirm.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(create_window, text="Họ và tên:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_fullname = tk.Entry(create_window)
        self.entry_fullname.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(create_window, text="Ngày sinh (YYYY-MM-DD):").grid(row=4, column=0, padx=5, pady=5)
        self.entry_dob = DateEntry(create_window, date_pattern='yyyy-mm-dd')
        self.entry_dob.grid(row=4, column=1, padx=5, pady=5)

        tk.Button(create_window, text="Tạo tài khoản", command=self.save_account).grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def save_account(self):
        username = self.entry_username.get()
        if file_method.is_username_unique(username):
            ids_load = file_method.load_available_ids("ids.txt")
            user_id = file_method.find_smallest_missing_id(ids_load)

            if user_id is not None:
                file_method.add_id_to_file(user_id, "ids.txt")
                account_data = {
                    "username": username,
                    "password": self.entry_password_new.get(),
                    "role": "member",
                    "id": user_id
                }
                file_method.save_data_json('accounts.json', account_data)
                user_data = {
                    "username": username,
                    "fullname": self.entry_fullname.get(),
                    "dob": self.entry_dob.get(),
                    "id": user_id,
                    "join_date": datetime.today().strftime('%Y-%m-%d'),
                    "activity_points": 0
                }
                file_method.save_data_json('user_details.json', user_data)
                messagebox.showinfo("Thông báo", "Tạo tài khoản thành công.")
                self.entry_username.master.destroy()
            else:
                messagebox.showerror("Lỗi", "Không có mã số nào khả dụng.")
        else:
            messagebox.showerror("Lỗi", "Tên tài khoản đã tồn tại.")


    def remove_account(self, username, id):
        # Xoá tài khoản từ file accounts.json
        data_login = file_method.load_data_json('accounts.json')
        for account in data_login:
            if account["username"] == username or account["id"] == id:
                file_method.delete_id_from_file(id, "ids.txt")
                data_login.remove(account)
                file_method.save_data_login('accounts.json', data_login)
                break

        # Xoá tài khoản từ file user_details.json
        data_details = file_method.load_data_json('user_details.json')
        for user in data_details:
            if user["username"] == username:
                data_details.remove(user)
                file_method.save_data_login('user_details.json', data_details)
                break

    def login(self):
        username = self.entry_user_name.get()
        password = self.entry_password.get()

        data = file_method.load_data_json('accounts.json')

        for account in data:
            if account["username"] == username and account["password"] == password:
                if account.get("role") == "admin":
                    messagebox.showinfo("Login", "Login successful as Admin")
                    self.root.destroy()
                    root2 = tk.Tk()
                    app = frm_admin.AdminForm(root2)
                    root2.mainloop()
                    return
                elif account.get("role") == "member":
                    messagebox.showinfo("Login", "Login successful as Member")
                    return
        messagebox.showerror("Login", "Login failed")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
