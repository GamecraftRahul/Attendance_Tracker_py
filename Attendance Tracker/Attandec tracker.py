# ===================================================
# ATTENDANCE TRACKER SYSTEM (FINAL FIXED VERSION - LIGHT & READABLE THEME)
# Python + ttkbootstrap + MySQL + SQLAlchemy + Pandas
# ===================================================

import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
from datetime import date
import pandas as pd
from sqlalchemy import create_engine, text

# -------------------- DATABASE CONFIG --------------------
DB_CONFIG = {
    'user': 'root',
    'password': 'RAHUL123',  # <-- Change this
    'host': 'localhost',
    'database': 'attendance_db'
}
DB_URL = f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
engine = create_engine(DB_URL, pool_pre_ping=True)


# -------------------- LOGIN WINDOW --------------------
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Attendance Tracker")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.safe_exit)

        tb.Label(self.root, text="Attendance Tracker Login",
                 bootstyle="inverse-primary", font=("Helvetica", 16, "bold")).pack(pady=20)

        self.username = tb.Entry(self.root, width=30)
        self.username.insert(0, "admin")
        self.username.pack(pady=5)

        self.password = tb.Entry(self.root, width=30, show="*")
        self.password.insert(0, "admin123")
        self.password.pack(pady=5)

        tb.Button(self.root, text="Login", bootstyle="success", command=self.login).pack(pady=15)

    def safe_exit(self):
        try:
            self.root.after_cancel(self.root.after_id) if hasattr(self.root, 'after_id') else None
        except:
            pass
        self.root.quit()
        self.root.destroy()

    def login(self):
        uname = self.username.get().strip()
        pwd = self.password.get().strip()

        try:
            with engine.connect() as conn:
                result = conn.execute(
                    text("SELECT * FROM admin WHERE username=:u AND password=:p"),
                    {"u": uname, "p": pwd}
                ).fetchone()

            if result:
                messagebox.showinfo("Login Success", f"Welcome, {uname}!")
                self.root.withdraw()
                self.open_dashboard()
            else:
                messagebox.showerror("Error", "Invalid credentials")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def open_dashboard(self):
        dashboard = tb.Toplevel(self.root)
        Dashboard(dashboard)
        dashboard.protocol("WM_DELETE_WINDOW", lambda: self.close_all(dashboard))

    def close_all(self, dashboard):
        try:
            dashboard.destroy()
        except:
            pass
        self.safe_exit()


# -------------------- DASHBOARD --------------------
class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Tracker Dashboard")
        self.root.geometry("1150x650")

        tb.Label(self.root, text="Attendance Tracker Dashboard",
                 font=("Helvetica", 20, "bold"), bootstyle="primary").pack(pady=15)

        frame = tb.Frame(self.root)
        frame.pack(pady=10)

        buttons = [
            ("Add Student", "info-outline", self.add_student_window),
            ("View Students", "secondary-outline", self.view_students),
            ("Mark Attendance", "success-outline", self.mark_attendance),
            ("View Attendance", "warning-outline", self.view_attendance),
            ("Day-to-Day View", "primary-outline", self.day_to_day_view),
            ("Attendance % Report", "danger-outline", self.attendance_percentage),
            ("Export to CSV", "light-outline", self.export_csv)
        ]

        for i, (text, style, cmd) in enumerate(buttons):
            tb.Button(frame, text=text, bootstyle=style, width=18, command=cmd).grid(row=0, column=i, padx=8, pady=5)

    # -------------------- ADD STUDENT --------------------
    def add_student_window(self):
        win = tb.Toplevel(self.root)
        win.title("Add New Student")
        win.geometry("400x400")

        tb.Label(win, text="Add Student Details", font=("Helvetica", 16, "bold"), bootstyle="primary").pack(pady=10)
        fields = ["Name", "Roll No", "Department", "Semester", "Contact", "Email"]
        entries = {}
        for f in fields:
            tb.Label(win, text=f).pack()
            entries[f] = tb.Entry(win, width=35)
            entries[f].pack(pady=3)

        def save_student():
            data = {f.lower().replace(" ", "_"): entries[f].get().strip() for f in fields}
            try:
                with engine.begin() as conn:
                    conn.execute(text("""
                        INSERT INTO students (name, roll_no, department, semester, contact, email)
                        VALUES (:name, :roll_no, :department, :semester, :contact, :email)
                    """), data)
                messagebox.showinfo("Success", "Student added successfully")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tb.Button(win, text="Save", bootstyle="success", command=save_student).pack(pady=10)

    # -------------------- VIEW STUDENTS --------------------
    def view_students(self):
        win = tb.Toplevel(self.root)
        win.title("All Students")
        win.geometry("800x400")

        tree = tb.Treeview(win, columns=("ID", "Name", "Roll", "Dept", "Sem", "Contact", "Email"), show='headings')
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack(fill=BOTH, expand=True)

        try:
            df = pd.read_sql("SELECT * FROM students", engine)
            for _, row in df.iterrows():
                tree.insert("", END, values=list(row))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # -------------------- MARK ATTENDANCE --------------------
    def mark_attendance(self):
        win = tb.Toplevel(self.root)
        win.title("Mark Attendance")
        win.geometry("850x500")

        tb.Label(win, text=f"Mark Attendance for {date.today()}",
                 font=("Helvetica", 16, "bold"), bootstyle="primary").pack(pady=10)
        tree = tb.Treeview(win, columns=("ID", "Name", "Roll", "Status"), show='headings', height=15)
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack(fill=BOTH, expand=True, pady=10)

        try:
            df = pd.read_sql("SELECT student_id, name, roll_no FROM students", engine)
            for _, s in df.iterrows():
                tree.insert("", END, values=(s.iloc[0], s.iloc[1], s.iloc[2], ""))
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        def set_status(status):
            for selected in tree.selection():
                tree.set(selected, column="Status", value=status)

        def save_attendance():
            today = date.today()
            try:
                with engine.begin() as conn:
                    for item in tree.get_children():
                        sid, name, roll, status = tree.item(item, "values")
                        if status:
                            conn.execute(text("""
                                INSERT INTO attendance (student_id, date, status)
                                VALUES (:sid, :d, :s)
                            """), {"sid": sid, "d": today, "s": status})
                messagebox.showinfo("Success", "Attendance saved successfully")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        btn_frame = tb.Frame(win)
        btn_frame.pack(pady=10)
        tb.Button(btn_frame, text="Present", bootstyle="success", command=lambda: set_status("Present")).grid(row=0, column=0, padx=5)
        tb.Button(btn_frame, text="Absent", bootstyle="danger", command=lambda: set_status("Absent")).grid(row=0, column=1, padx=5)
        tb.Button(btn_frame, text="Late", bootstyle="warning", command=lambda: set_status("Late")).grid(row=0, column=2, padx=5)
        tb.Button(btn_frame, text="Save Attendance", bootstyle="primary", command=save_attendance).grid(row=0, column=3, padx=10)

    # -------------------- VIEW ATTENDANCE --------------------
    def view_attendance(self):
        win = tb.Toplevel(self.root)
        win.title("Attendance Records")
        win.geometry("900x500")

        tree = tb.Treeview(win, columns=("ID", "Name", "Roll", "Date", "Status"), show='headings')
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack(fill=BOTH, expand=True)

        query = """
            SELECT a.attendance_id, s.name, s.roll_no, a.date, a.status
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
            ORDER BY a.date DESC
        """
        try:
            df = pd.read_sql(query, engine)
            for _, row in df.iterrows():
                tree.insert("", END, values=list(row))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # -------------------- DAY-TO-DAY VIEW --------------------
    def day_to_day_view(self):
        win = tb.Toplevel(self.root)
        win.title("Day-to-Day Attendance View")
        win.geometry("1000x500")

        query = """
            SELECT s.name, s.roll_no, a.date, a.status
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
            ORDER BY a.date
        """
        df = pd.read_sql(query, engine)
        if df.empty:
            messagebox.showinfo("Info", "No attendance records found")
            return

        pivot_df = df.pivot_table(index=["roll_no", "name"], columns="date", values="status", aggfunc="first", fill_value="-")

        tree = tb.Treeview(win, columns=list(pivot_df.columns.insert(0, "Student")), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=str(col))
            tree.column(col, width=100)
        tree.pack(fill=BOTH, expand=True)

        for idx, row in pivot_df.iterrows():
            tree.insert("", END, values=[f"{idx[1]} ({idx[0]})"] + row.tolist())

    # -------------------- ATTENDANCE PERCENTAGE --------------------
    def attendance_percentage(self):
        win = tb.Toplevel(self.root)
        win.title("Attendance Percentage Report")
        win.geometry("750x400")

        query = """
            SELECT s.student_id, s.name, s.roll_no, a.status
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
        """
        df = pd.read_sql(query, engine)
        if df.empty:
            messagebox.showinfo("Info", "No attendance data available")
            return

        report = df.groupby(["roll_no", "name"]).status.value_counts().unstack(fill_value=0)
        report["Total Days"] = report.sum(axis=1)
        report["% Present"] = round((report.get("Present", 0) / report["Total Days"]) * 100, 2)

        tree = tb.Treeview(win, columns=["Roll No", "Name", "Present", "Absent", "Late", "Total Days", "% Present"], show='headings')
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack(fill=BOTH, expand=True)

        for idx, row in report.iterrows():
            tree.insert("", END, values=[
                idx[0], idx[1],
                row.get("Present", 0),
                row.get("Absent", 0),
                row.get("Late", 0),
                row["Total Days"],
                f"{row['% Present']}%"
            ])

    # -------------------- EXPORT TO CSV --------------------
    def export_csv(self):
        query = """
            SELECT s.name, s.roll_no, a.date, a.status
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
        """
        df = pd.read_sql(query, engine)
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file:
            df.to_csv(file, index=False)
            messagebox.showinfo("Export Success", f"Attendance exported to {file}")


# -------------------- MAIN --------------------
if __name__ == "__main__":
    # 🟢 Changed theme from 'superhero' (dark) to 'flatly' (light, readable)
    app = tb.Window(themename="flatly")
    LoginWindow(app)
    app.mainloop()
