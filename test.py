import tkinter as tk
from tkinter import messagebox, ttk
from Ham_json import load_data, save_data, save_member_info, format_member_id, delete_member_info

class MemberManager(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.cols_of_members = ('member_id', 'full_name', 'dob', 'date_join', 'position', 'activity_points')
        self.tree_of_members = ttk.Treeview(self, columns=self.cols_of_members, show='headings')

        for col in self.cols_of_members:
            self.tree_of_members.heading(col, text=col)
            self.tree_of_members.column(col, width=100)

        data = load_data('member_info.json')
        for member in data["members"]:
            self.tree_of_members.insert("", "end", values=(member["member_id"], member["full_name"], member["dob"], member["date_join"], member["position"], member["activity_points"]))

        self.tree_of_members.pack(expand=True, fill=tk.BOTH)

        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X)

        tk.Button(button_frame, text="Thêm Thành viên", command=self.add_member).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(button_frame, text="Xóa Thành viên", command=self.delete_member).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(button_frame, text="Cập nhật Thành viên", command=self.update_member).pack(side=tk.LEFT, padx=10, pady=5)

    def add_member(self):
        add_member_window = AddMemberWindow(self.master, self.tree_of_members)

    def delete_member(self):
        selected_item = self.tree_of_members.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một thành viên để xóa")
            return
        item = self.tree_of_members.item(selected_item)
        member_id = item['values'][0]
        member_id = format_member_id(member_id)
        delete_member_info('member_info.json', member_id)
        self.tree_of_members.delete(selected_item)
        messagebox.showinfo("Thông báo", "Xóa thành viên thành công")

    def update_member(self):
        selected_item = self.tree_of_members.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một thành viên để cập nhật")
            return
        update_member_window = UpdateMemberWindow(self.master, self.tree_of_members, selected_item)

class AddMemberWindow(tk.Toplevel):
    def __init__(self, master, tree_of_members):
        super().__init__(master)
        self.title("Thêm Thành viên")
        self.geometry("400x400")

        self.labels = ["Họ và tên", "Ngày sinh (YYYY-MM-DD)", "Ngày gia nhập (YYYY-MM-DD)", "Chức vụ", "Điểm hoạt động"]
        self.entries = []

        for label in self.labels:
            frame = tk.Frame(self)
            frame.pack(fill=tk.X, padx=10, pady=5)
            tk.Label(frame, text=label).pack(side=tk.LEFT)
            entry = tk.Entry(frame)
            entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            self.entries.append(entry)

        tk.Button(self, text="Lưu", command=lambda: self.save_new_member(tree_of_members)).pack(pady=10)

    def save_new_member(self, tree_of_members):
        new_member = {
            "full_name": self.entries[0].get(),
            "dob": self.entries[1].get(),
            "date_join": self.entries[2].get(),
            "position": self.entries[3].get(),
            "activity_points": int(self.entries[4].get())
        }
        save_member_info('member_info.json', new_member)
        messagebox.showinfo("Thông báo", "Thêm thành viên thành công")
        self.destroy()
        tree_of_members.update_members_view()

class UpdateMemberWindow(tk.Toplevel):
    def __init__(self, master, tree_of_members, selected_item):
        super().__init__(master)
        self.title("Cập nhật Thành viên")
        self.geometry("400x400")

        self.selected_item = selected_item
        item = tree_of_members.item(selected_item)
        member_id = item['values'][0]
        member_id = format_member_id(member_id)
        data = load_data('member_info.json')
        self.member = next((member for member in data["members"] if member["member_id"] == member_id), None)

        self.labels = ["Họ và tên", "Ngày sinh (YYYY-MM-DD)", "Ngày gia nhập (YYYY-MM-DD)", "Chức vụ", "Điểm hoạt động"]
        self.entries = []

        for label, key in zip(self.labels, ["full_name", "dob", "date_join", "position", "activity_points"]):
            frame = tk.Frame(self)
            frame.pack(fill=tk.X, padx=10, pady=5)
            tk.Label(frame, text=label).pack(side=tk.LEFT)
            entry = tk.Entry(frame)
            entry.insert(0, self.member[key])
            entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            self.entries.append(entry)

        tk.Button(self, text="Lưu", command=self.save_updated_member).pack(pady=10)

    def save_updated_member(self):
        self.member["full_name"] = self.entries[0].get()
        self.member["dob"] = self.entries[1].get()
        self.member["date_join"] = self.entries[2].get()
        self.member["position"] = self.entries[3].get()
        self.member["activity_points"] = int(self.entries[4].get())
        save_data('member_info.json', {"members": [self.member]})
        messagebox.showinfo("Thông báo", "Cập nhật thành viên thành công")
        self.destroy()
        self.tree_of_members.update_members_view()
