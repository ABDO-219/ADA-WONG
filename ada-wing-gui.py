#!/usr/bin/env python3
"""واجهة رسومية لأداة ADA-WING."""

import os
import shutil
import subprocess
import sys
import threading

try:
    import tkinter as tk
    from tkinter import messagebox, scrolledtext
except ModuleNotFoundError:
    print("خطأ: مكتبة Tkinter غير مثبتة. قم بتشغيل: sudo apt update && sudo apt install -y python3-tk", file=sys.stderr)
    sys.exit(1)

APP_TITLE = "ADA-WING GUI"


def find_ada_wing_executable():
    path = shutil.which("ada-wing")
    if path:
        return path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    local_path = os.path.join(current_dir, "ada-wing")
    if os.path.isfile(local_path) and os.access(local_path, os.X_OK):
        return local_path
    return None


class AdaWingGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("820x600")
        self.resizable(True, True)

        self.ada_wing_path = find_ada_wing_executable()
        if not self.ada_wing_path:
            messagebox.showerror("خطأ", "تعذر العثور على برنامج ADA-WING. تأكد من تثبيته أو تشغيل هذا الملف من نفس المجلد.")
            self.destroy()
            return

        self.create_widgets()

    def create_widgets(self):
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=8)

        actions = [
            ("معلومات النظام", self.action_sysinfo),
            ("تحديث النظام", self.action_update),
            ("تنظيف النظام", self.action_clean),
            ("فحص الشبكة", self.action_netcheck),
            ("الأقراص", self.action_disk),
            ("المراقبة", self.action_monitor),
        ]

        for label, command in actions:
            btn = tk.Button(button_frame, text=label, width=14, command=command)
            btn.pack(side=tk.LEFT, padx=4, pady=2)

        form_frame = tk.Frame(self)
        form_frame.pack(fill=tk.X, padx=10, pady=8)

        self.search_var = tk.StringVar()
        self.service_action_var = tk.StringVar(value="status")
        self.service_name_var = tk.StringVar()
        self.user_action_var = tk.StringVar(value="add")
        self.user_name_var = tk.StringVar()
        self.find_pattern_var = tk.StringVar()
        self.find_path_var = tk.StringVar(value="/")
        self.net_host_var = tk.StringVar(value="8.8.8.8")

        self.add_form_row(form_frame, "بحث حزمة:", self.search_var, "البحث", self.action_pkg_search)
        self.add_form_row(form_frame, "اختبار ping:", self.net_host_var, "تنفيذ", self.action_netcheck)
        self.add_service_row(form_frame)
        self.add_user_row(form_frame)
        self.add_find_row(form_frame)

        self.output_box = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=18, state=tk.DISABLED)
        self.output_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.status_label = tk.Label(self, text="جاهز", anchor="w")
        self.status_label.pack(fill=tk.X, padx=10, pady=(0, 8))

    def add_form_row(self, parent, label_text, variable, button_text, command):
        row = tk.Frame(parent)
        row.pack(fill=tk.X, pady=2)
        tk.Label(row, text=label_text, width=12, anchor="w").pack(side=tk.LEFT)
        tk.Entry(row, textvariable=variable, width=30).pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(row, text=button_text, width=10, command=command).pack(side=tk.LEFT)

    def add_service_row(self, parent):
        row = tk.Frame(parent)
        row.pack(fill=tk.X, pady=2)
        tk.Label(row, text="خدمة:", width=12, anchor="w").pack(side=tk.LEFT)
        service_actions = ["start", "stop", "restart", "status", "enable", "disable"]
        tk.OptionMenu(row, self.service_action_var, *service_actions).pack(side=tk.LEFT, padx=(0, 6))
        tk.Entry(row, textvariable=self.service_name_var, width=20).pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(row, text="تشغيل", width=10, command=self.action_service).pack(side=tk.LEFT)

    def add_user_row(self, parent):
        row = tk.Frame(parent)
        row.pack(fill=tk.X, pady=2)
        tk.Label(row, text="مستخدم:", width=12, anchor="w").pack(side=tk.LEFT)
        user_actions = ["add", "remove"]
        tk.OptionMenu(row, self.user_action_var, *user_actions).pack(side=tk.LEFT, padx=(0, 6))
        tk.Entry(row, textvariable=self.user_name_var, width=20).pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(row, text="تشغيل", width=10, command=self.action_user).pack(side=tk.LEFT)

    def add_find_row(self, parent):
        row = tk.Frame(parent)
        row.pack(fill=tk.X, pady=2)
        tk.Label(row, text="بحث ملف:", width=12, anchor="w").pack(side=tk.LEFT)
        tk.Entry(row, textvariable=self.find_pattern_var, width=18).pack(side=tk.LEFT, padx=(0, 6))
        tk.Entry(row, textvariable=self.find_path_var, width=18).pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(row, text="بحث", width=10, command=self.action_find).pack(side=tk.LEFT)

    def run_ada_command(self, args):
        self.append_output(f"تشغيل: ada-wing {' '.join(args)}\n\n")
        self.set_status("جارٍ التنفيذ...")

        def worker():
            try:
                result = subprocess.run(
                    [self.ada_wing_path] + args,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                )
                self.append_output(result.stdout)
            except subprocess.CalledProcessError as exc:
                self.append_output(exc.output or f"فشل الأمر: {' '.join(args)}\n")
            finally:
                self.set_status("جاهز")

        threading.Thread(target=worker, daemon=True).start()

    def append_output(self, text):
        def update():
            self.output_box.configure(state=tk.NORMAL)
            self.output_box.insert(tk.END, text)
            self.output_box.see(tk.END)
            self.output_box.configure(state=tk.DISABLED)

        self.after(0, update)

    def set_status(self, text):
        self.after(0, lambda: self.status_label.config(text=text))

    def action_sysinfo(self):
        self.run_ada_command(["sysinfo"])

    def action_update(self):
        self.run_ada_command(["update"])

    def action_clean(self):
        self.run_ada_command(["clean"])

    def action_netcheck(self):
        host = self.net_host_var.get().strip() or "8.8.8.8"
        self.run_ada_command(["netcheck", "--host", host])

    def action_pkg_search(self):
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning("تنبيه", "ادخل نص البحث أولاً.")
            return
        self.run_ada_command(["pkg-search", query])

    def action_service(self):
        service = self.service_name_var.get().strip()
        if not service:
            messagebox.showwarning("تنبيه", "ادخل اسم الخدمة أولاً.")
            return
        self.run_ada_command(["service", self.service_action_var.get(), service])

    def action_user(self):
        username = self.user_name_var.get().strip()
        if not username:
            messagebox.showwarning("تنبيه", "ادخل اسم المستخدم أولاً.")
            return
        self.run_ada_command(["user", self.user_action_var.get(), username])

    def action_find(self):
        pattern = self.find_pattern_var.get().strip()
        path = self.find_path_var.get().strip() or "/"
        if not pattern:
            messagebox.showwarning("تنبيه", "ادخل نمط البحث أولاً.")
            return
        self.run_ada_command(["find", pattern, "--path", path])

    def action_disk(self):
        self.run_ada_command(["disk"])

    def action_monitor(self):
        self.run_ada_command(["monitor"])


def main():
    try:
        app = AdaWingGui()
        app.mainloop()
    except tk.TclError as exc:
        if "no display name" in str(exc).lower() or "display" in str(exc).lower():
            print("خطأ: لا يوجد عرض رسومي متاح. شغّل البرنامج من جلسة سطح مكتب أو من قائمة التطبيقات.", file=sys.stderr)
            sys.exit(1)
        raise


if __name__ == "__main__":
    main()
