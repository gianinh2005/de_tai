import tkinter as tk
from tkinter import ttk
import file_method

class AdminForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.geometry("1200x600")

        # Create the main frame
        main_frame = tk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid layout for the root window
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Create a left frame for the tabs
        left_frame = tk.Frame(main_frame, width=200)
        left_frame.grid(row=0, column=0, sticky="ns")
        left_frame.grid_propagate(False)

        # Create buttons for member and event management
        self.manage_member_btn = tk.Button(left_frame, text="Quản lý thành viên", command=self.show_manage_member)
        self.manage_member_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.manage_event_btn = tk.Button(left_frame, text="Quản lý sự kiện", command=self.show_manage_event)
        self.manage_event_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # Create a middle frame for the tree views
        middle_frame = tk.Frame(main_frame)
        middle_frame.grid(row=0, column=1, sticky="nsew")

        # Configure grid layout for the middle frame
        middle_frame.grid_rowconfigure(0, weight=1)
        middle_frame.grid_columnconfigure(0, weight=1)

        # Create the Treeview for managing members
        self.member_tree = ttk.Treeview(middle_frame, columns=("ID", "Fullname", "DOB", "Join Date", "Activity Points"), show="headings")
        self.member_tree.heading("ID", text="ID")
        self.member_tree.heading("Fullname", text="Fullname")
        self.member_tree.heading("DOB", text="DOB")
        self.member_tree.heading("Join Date", text="Join Date")
        self.member_tree.heading("Activity Points", text="Activity Points")
        self.member_tree.grid(row=0, column=0, sticky="nsew")

        # Create the Treeview for managing events (empty for now)
        self.event_tree = ttk.Treeview(middle_frame, columns=("ID", "Event Name", "Date", "Location"), show="headings")
        self.event_tree.heading("ID", text="ID")
        self.event_tree.heading("Event Name", text="Event Name")
        self.event_tree.heading("Date", text="Date")
        self.event_tree.heading("Location", text="Location")

        # Create a right frame for action buttons
        right_frame = tk.Frame(main_frame, width=200)
        right_frame.grid(row=0, column=2, sticky="ns")
        right_frame.grid_propagate(False)

        # Create action buttons for member management
        self.add_btn = tk.Button(right_frame, text="Thêm", command=self.add_item)
        self.add_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.edit_btn = tk.Button(right_frame, text="Sửa", command=self.edit_item)
        self.edit_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.delete_btn = tk.Button(right_frame, text="Xoá", command=self.delete_item)
        self.delete_btn.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.search_btn = tk.Button(right_frame, text="Tìm kiếm", command=self.search_item)
        self.search_btn.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        # Placeholder for switching views
        self.current_view = None
        self.show_manage_member()

    def show_manage_member(self):
        self.current_view = "members"
        self.event_tree.grid_forget()
        self.member_tree.grid(row=0, column=0, sticky="nsew")
        self.load_data_to_treeview('user_details.json', self.member_tree)

    def show_manage_event(self):
        self.current_view = "events"
        self.member_tree.grid_forget()
        self.event_tree.grid(row=0, column=0, sticky="nsew")

    def load_data_to_treeview(self, filename, treeview):
        # Clear the Treeview
        treeview.delete(*treeview.get_children())

        # Load data from file
        data = file_method.load_data_json(filename)

        # Insert data into Treeview, excluding the "username" field
        for item in data:
            treeview.insert("", "end", values=(item["id"], item["fullname"], item["dob"], item["join_date"], item["activity_points"]))

    def add_item(self):
        # Add item logic here
        pass

    def edit_item(self):
        # Edit item logic here
        pass

    def delete_item(self):
        # Delete item logic here
        pass

    def search_item(self):
        # Search item logic here
        pass