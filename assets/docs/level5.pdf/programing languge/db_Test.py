#!/usr/bin/env python3
# uefa_manager_gui.py
# Tkinter GUI manager for uefa_project (dark blue theme)
# Supports CRUD for tables and Reports (staff salaries, team player count, total staff salaries)

import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, messagebox
import traceback

# ---------------- DB CONFIG - عدل لو لزم ----------------
DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = "H.s.s123"
DB_DATABASE = "uefa_project"
# --------------------------------------------------------

# Mapping common FK column names to referenced table names (used to populate comboboxes)
FK_GUESS_MAP = {
    "U_name": "UEFA",
    "T_name": "Team",
    "C_num": "Championships",
    "P_id": "Person",
    "M_id": "Matches"
}

# --------- UI Colors (Dark Blue Theme) ----------
COLOR_BG = "#0A1A2F"
COLOR_PANEL = "#0F2B49"
COLOR_BTN = "#114a8d"
COLOR_BTN_HOVER = "#165fb3"
COLOR_TEXT = "#FFFFFF"
COLOR_ACCENT = "#1E90FF"
# ------------------------------------------------

def create_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE
        )
        return conn
    except Error as e:
        messagebox.showerror("DB Connection Error", f"Could not connect to database:\n{e}")
        return None

# Utility: get list of tables in DB
def get_tables(conn):
    cur = conn.cursor()
    cur.execute("SHOW TABLES;")
    rows = cur.fetchall()
    cur.close()
    return [r[0] for r in rows]

# Utility: describe table columns (name, type, key, extra)
def describe_table(conn, table):
    cur = conn.cursor()
    cur.execute(f"DESCRIBE `{table}`;")
    rows = cur.fetchall()
    cur.close()
    # rows: Field, Type, Null, Key, Default, Extra
    cols = []
    for r in rows:
        cols.append({
            "Field": r[0],
            "Type": r[1],
            "Null": r[2],
            "Key": r[3],
            "Default": r[4],
            "Extra": r[5]
        })
    return cols

# Create main app window with dark theme styles
class UEFAApp:
    def __init__(self, root):
        self.root = root
        root.title("UEFA Project Manager")
        root.geometry("950x700")
        root.configure(bg=COLOR_BG)

        # Style
        style = ttk.Style()
        style.theme_use('clam')  # use clam for better customization
        style.configure("TLabel", background=COLOR_BG, foreground=COLOR_TEXT, font=("Helvetica", 11))
        style.configure("Header.TLabel", font=("Helvetica", 18, "bold"))
        style.configure("TButton", background=COLOR_BTN, foreground=COLOR_TEXT, font=("Helvetica", 10))
        style.configure("Treeview", background="#072033", foreground=COLOR_TEXT, fieldbackground="#072033")
        style.configure("Treeview.Heading", background=COLOR_PANEL, foreground=COLOR_TEXT, font=("Helvetica", 10, "bold"))
        style.map("TButton", background=[("active", COLOR_BTN_HOVER)])

        header = ttk.Label(root, text="UEFA Project - Database Manager", style="Header.TLabel")
        header.pack(pady=12)

        # Frames
        top_frame = tk.Frame(root, bg=COLOR_PANEL, pady=10, padx=10)
        top_frame.pack(fill=tk.X, padx=12, pady=6)

        ttk.Label(top_frame, text=f"Connected DB: {DB_DATABASE}", style="TLabel").pack(side=tk.LEFT, padx=8)

        btn_report_frame = tk.Frame(top_frame, bg=COLOR_PANEL)
        btn_report_frame.pack(side=tk.RIGHT)

        ttk.Button(btn_report_frame, text="Staff Salaries (Desc)", command=self.show_staff_salaries).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_report_frame, text="Team Player Count", command=self.show_team_player_count).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_report_frame, text="Total Staff Salary", command=self.show_total_staff_salary).pack(side=tk.LEFT, padx=6)

        # Main content: left side buttons for tables, right side tabbed area
        content = tk.Frame(root, bg=COLOR_BG)
        content.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)

        left = tk.Frame(content, width=220, bg=COLOR_PANEL)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0,8))
        left.pack_propagate(False)

        ttk.Label(left, text="Tables", style="TLabel").pack(pady=(6,8))

        # Build table buttons dynamically
        conn = create_connection()
        if conn is None:
            root.destroy()
            return
        tables = get_tables(conn)
        conn.close()

        # right side: Notebook (tabs)
        self.notebook = ttk.Notebook(content)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # create a tab for each table
        self.table_frames = {}  # table_name -> frame object
        for t in tables:
            btn = ttk.Button(left, text=t, width=24, command=lambda name=t: self.open_table_tab(name))
            btn.pack(pady=4)

        # add a Dashboard tab
        dash = tk.Frame(self.notebook, bg=COLOR_BG)
        self.notebook.add(dash, text="Dashboard")
        ttk.Label(dash, text="Welcome to UEFA Project Manager", style="TLabel").pack(pady=20)

        # Info area on dashboard
        self.dashboard_text = tk.Text(dash, height=20, bg="#071B31", fg=COLOR_TEXT)
        self.dashboard_text.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        self.log("App started. Press any table button to open CRUD tab.\nReports available on top-right.")

    def log(self, message):
        self.dashboard_text.insert(tk.END, message + "\n")
        self.dashboard_text.see(tk.END)

    def open_table_tab(self, table_name):
        # If tab already open, select it
        for idx in range(len(self.notebook.tabs())):
            tab_text = self.notebook.tab(idx, "text")
            if tab_text == table_name:
                self.notebook.select(idx)
                return

        # create new tab frame
        frame = tk.Frame(self.notebook, bg=COLOR_BG)
        self.notebook.add(frame, text=table_name)
        self.notebook.select(frame)
        self.table_frames[table_name] = frame

        # Build CRUD UI inside the tab
        self.build_crud_tab(frame, table_name)

    def build_crud_tab(self, parent, table_name):
        conn = create_connection()
        if conn is None:
            return

        cols_info = describe_table(conn, table_name)
        columns = [c["Field"] for c in cols_info]
        pk_col = None
        for c in cols_info:
            if c["Key"] == "PRI":
                pk_col = c["Field"]
                break
        if not pk_col:
            pk_col = columns[0]  # fallback

        top = tk.Frame(parent, bg=COLOR_BG)
        top.pack(fill=tk.X, pady=8, padx=8)

        # Buttons
        btn_add = ttk.Button(top, text="Add", command=lambda: self.add_record(table_name, cols_info, tree, entries))
        btn_update = ttk.Button(top, text="Update", command=lambda: self.update_record(table_name, cols_info, tree, entries))
        btn_delete = ttk.Button(top, text="Delete", command=lambda: self.delete_record(table_name, cols_info, tree))
        btn_refresh = ttk.Button(top, text="Refresh", command=lambda: self.load_table_data(table_name, tree))

        btn_add.pack(side=tk.LEFT, padx=6)
        btn_update.pack(side=tk.LEFT, padx=6)
        btn_delete.pack(side=tk.LEFT, padx=6)
        btn_refresh.pack(side=tk.LEFT, padx=6)

        # Entry form area (scrollable)
        form_frame = tk.Frame(parent, bg=COLOR_BG)
        form_frame.pack(fill=tk.X, padx=8, pady=6)

        entries = {}  # column -> widget

        # For better layout, use two columns of fields
        left_col = tk.Frame(form_frame, bg=COLOR_BG)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right_col = tk.Frame(form_frame, bg=COLOR_BG)
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for i, col in enumerate(columns):
            target = left_col if i % 2 == 0 else right_col
            lbl = ttk.Label(target, text=col)
            lbl.pack(anchor="w", padx=6, pady=2)

            # If column likely FK, use Combobox populated from referenced table
            if col in FK_GUESS_MAP:
                ref_table = FK_GUESS_MAP[col]
                # fetch values from ref_table
                try:
                    cur = conn.cursor()
                    cur.execute(f"SELECT DISTINCT `{col}` FROM `{ref_table}`;")
                    # sometimes FK name differs, try selecting a PK from referenced table
                    vals = [r[0] for r in cur.fetchall()] if cur.description else []
                    cur.close()
                except Exception:
                    # fallback: select first column values
                    try:
                        cur = conn.cursor()
                        cur.execute(f"SELECT `{list(describe_table(conn, ref_table))[0]['Field']}` FROM `{ref_table}` LIMIT 200;")
                        vals = [r[0] for r in cur.fetchall()]
                        cur.close()
                    except Exception:
                        vals = []
                combo = ttk.Combobox(target, values=vals, width=30)
                combo.pack(anchor="w", padx=6, pady=2)
                entries[col] = combo
            else:
                ent = ttk.Entry(target, width=36)
                ent.pack(anchor="w", padx=6, pady=2)
                entries[col] = ent

        # Treeview to display data
        tree_frame = tk.Frame(parent, bg=COLOR_BG)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for c in columns:
            tree.heading(c, text=c)
            tree.column(c, width=120, anchor="center")
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # when selecting a row, populate entries
        def on_select(e):
            sel = tree.focus()
            if not sel:
                return
            vals = tree.item(sel)["values"]
            for i, col in enumerate(columns):
                widget = entries[col]
                try:
                    widget_val = "" if vals[i] is None else str(vals[i])
                except Exception:
                    widget_val = ""
                if isinstance(widget, ttk.Combobox):
                    widget.set(widget_val)
                else:
                    widget.delete(0, tk.END)
                    widget.insert(0, widget_val)

        tree.bind("<<TreeviewSelect>>", on_select)

        # initial load
        self.load_table_data(table_name, tree)

        conn.close()

    def load_table_data(self, table_name, tree):
        # clear tree
        for r in tree.get_children():
            tree.delete(r)

        conn = create_connection()
        if conn is None:
            return

        cur = conn.cursor()
        try:
            cur.execute(f"SELECT * FROM `{table_name}`;")
            rows = cur.fetchall()
            # set columns if empty
            for row in rows:
                tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data:\n{e}")
        finally:
            cur.close()
            conn.close()

    def add_record(self, table_name, cols_info, tree, entries):
        conn = create_connection()
        if conn is None:
            return
        cols = [c["Field"] for c in cols_info]
        values = []
        for c in cols:
            w = entries[c]
            v = w.get()
            if v == "":
                v = None
            values.append(v)
        placeholders = ",".join(["%s"] * len(cols))
        sql = f"INSERT INTO `{table_name}` ({', '.join(['`'+c+'`' for c in cols])}) VALUES ({placeholders});"
        cur = conn.cursor()
        try:
            cur.execute(sql, values)
            conn.commit()
            messagebox.showinfo("Success", "Row added.")
            self.load_table_data(table_name, tree)
        except Exception as e:
            messagebox.showerror("Insert Error", f"{e}")
        finally:
            cur.close()
            conn.close()

    def delete_record(self, table_name, cols_info, tree):
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Select", "Please select a row to delete.")
            return
        values = tree.item(sel)["values"]
        pk_col = None
        for c in cols_info:
            if c["Key"] == "PRI":
                pk_col = c["Field"]
                break
        if not pk_col:
            pk_col = cols_info[0]["Field"]
        pk_index = [c["Field"] for c in cols_info].index(pk_col)
        pk_value = values[pk_index]
        if messagebox.askyesno("Confirm", f"Delete row where {pk_col} = {pk_value}?"):
            conn = create_connection()
            if conn is None:
                return
            cur = conn.cursor()
            try:
                cur.execute(f"DELETE FROM `{table_name}` WHERE `{pk_col}` = %s;", (pk_value,))
                conn.commit()
                messagebox.showinfo("Deleted", "Row deleted.")
                self.load_table_data(table_name, tree)
            except Exception as e:
                messagebox.showerror("Delete Error", f"{e}")
            finally:
                cur.close()
                conn.close()

    def update_record(self, table_name, cols_info, tree, entries):
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Select", "Select a row first.")
            return
        values = tree.item(sel)["values"]
        cols = [c["Field"] for c in cols_info]
        pk_col = None
        for c in cols_info:
            if c["Key"] == "PRI":
                pk_col = c["Field"]
                break
        if not pk_col:
            pk_col = cols[0]
        pk_index = cols.index(pk_col)
        pk_value = values[pk_index]

        new_vals = []
        for c in cols:
            w = entries[c]
            v = w.get()
            if v == "":
                v = None
            new_vals.append(v)

        update_pairs = ", ".join([f"`{c}` = %s" for c in cols])
        sql = f"UPDATE `{table_name}` SET {update_pairs} WHERE `{pk_col}` = %s;"
        conn = create_connection()
        if conn is None:
            return
        cur = conn.cursor()
        try:
            cur.execute(sql, new_vals + [pk_value])
            conn.commit()
            messagebox.showinfo("Updated", "Row updated successfully.")
            self.load_table_data(table_name, tree)
        except Exception as e:
            messagebox.showerror("Update Error", f"{e}")
        finally:
            cur.close()
            conn.close()

    # ---------------- Reports ----------------
    def show_staff_salaries(self):
        conn = create_connection()
        if conn is None:
            return
        cur = conn.cursor()
        try:
            # Attempt to join staff -> Person to get names and salaries, order desc
            q = """
            SELECT p.P_name, s.Salary, s.job
            FROM `Staff` s
            JOIN `Person` p ON s.P_id = p.P_id
            ORDER BY s.Salary DESC
            LIMIT 200;
            """
            cur.execute(q)
            rows = cur.fetchall()
            # show in popup
            self.show_result_window("Staff Salaries (Desc)", ["P_name", "Salary", "job"], rows)
        except Exception as e:
            messagebox.showerror("Error", f"Report failed:\n{e}")
        finally:
            cur.close()
            conn.close()

    def show_team_player_count(self):
        conn = create_connection()
        if conn is None:
            return
        cur = conn.cursor()
        try:
            q = """
            SELECT t.T_name, COUNT(p.P_id) as player_count
            FROM `Team` t
            LEFT JOIN `Person` pe ON pe.T_name = t.T_name
            LEFT JOIN `Players` p ON p.P_id = pe.P_id
            GROUP BY t.T_name
            ORDER BY player_count DESC;
            """
            cur.execute(q)
            rows = cur.fetchall()
            self.show_result_window("Team Player Count", ["Team", "Player Count"], rows)
        except Exception as e:
            messagebox.showerror("Error", f"Report failed:\n{e}")
        finally:
            cur.close()
            conn.close()

    def show_total_staff_salary(self):
        conn = create_connection()
        if conn is None:
            return
        cur = conn.cursor()
        try:
            q = "SELECT SUM(Salary) FROM `Staff`;"
            cur.execute(q)
            total = cur.fetchone()[0]
            messagebox.showinfo("Total Staff Salary", f"Total Staff Salary = {total}")
        except Exception as e:
            messagebox.showerror("Error", f"Report failed:\n{e}")
        finally:
            cur.close()
            conn.close()

    def show_result_window(self, title, columns, rows):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("600x400")
        # treeview
        tree = ttk.Treeview(win, columns=columns, show="headings")
        for c in columns:
            tree.heading(c, text=c)
            tree.column(c, width=150, anchor="center")
        tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        for r in rows:
            tree.insert("", tk.END, values=r)


def main():
    root = tk.Tk()
    app = UEFAApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
