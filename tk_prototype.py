import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Any
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Event
import os
@dataclass
class FileState:
    file_path: Optional[Path] = None
    file_name: Optional[str] = None
    is_modified: bool = False
    file_exists: bool = False

class AdorableKatze:
    def __init__(self):
        # run function
        self.file_state = FileState(
            file_path = None,
            file_name = None,
            is_modified = False,
            file_exists = False
        )
        self.original_content = ""
        self.setup_interface()
    def setup_interface(self):
        # init win
        self.root = tk.Tk()
        self.root.title("adorable_katze")
        self.root.geometry("800x600")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.Menu_bar()
        self.Main_frame()
        self.Status_bar()
    def Menu_bar(self):
        # init bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar)
        menubar.add_cascade(label="file", menu=file_menu)
        file_menu.add_command(label="new", command=self.new)
        file_menu.add_command(label="open file", command=self.open_file)
        file_menu.add_command(label="open folder", command=self.open_folder)
        file_menu.add_command(label="save", command=self.save)
        file_menu.add_command(label="save as", command=self.save_as)
    def new(self):
        if self.file_state.is_modified:
            save_changes = messagebox.askyesnocancel(
                "Unsaved changes",
                "Save changes to current file ?"
            )
            if save_changes == None:
                return
            elif save_changes:
                if not self.save():
                    return
        self.text.delete(1.0, tk.END)
        self.file_state = FileState()
        self.update_title()

    def open_file(self):
        if self.file_state.is_modified:
            if not self.save():
                return
        file_path = filedialog.askopenfilename(
            title="select file",
            filetypes=[
                ("all", "*.*")
            ]
        )
        if not file_path:
            return
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            self.text.delete(1.0, tk.END)
            self.text.insert(1.0, content)
            self.file_state = FileState(
                file_path = Path(file_path),
                file_name = os.path.basename(file_path),
                is_modified = False,
                file_exists = True
            )
            self.original_content = content
            self.text.edit_modified(False)
            self.update_title()
            if hasattr(self, 'update_statusbar'):
                self.update_statusbar()
            self.text.focus_set()
        except Exception as e:
            messagebox.showerror("Error", f"an error occurred: {str(e)}")
    def update_statusbar(self):
        status = "Ready"
        if self.file_state.file_name:
            status = f"Editing: {self.file_state.file_name}"
        if self.file_state.is_modified:
            status += "* Modified"
        self.status_var.set(status)
    def open_folder(self):
        pass
    def save(self):
        if not self.file_state.file_path:
            return self.save_as()
        try:
            content = self.text.get(1.0, tk.END)
            with open(self.file_state.file_path, "w", encoding="utf-8") as file:
                file.write(content.rstrip())
            self.file_state.is_modified = False
            self.original_content = content
            self.text.edit_modified(False)
            self.update_title()
            self.update_statusbar()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"an error occurred: {str(e)}")
            return False
    def save_as(self):
        file_path = filedialog.asksaveasfilename(
            title="Save as",
            filetypes=[("all", "*.*")]
        )
        if not file_path:
            return False
        try:
            content = self.text.get(1.0, tk.END)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content.rstrip())
            self.file_state = FileState(
                file_path = Path(file_path),
                file_name = os.path.basename(file_path),
                is_modified = False,
                file_exists = True
            )
            self.original_content = content
            self.text.edit_modified(False)
            self.update_title()
            self.update_statusbar()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"an error occurred: {str(e)}")
            return False

    def Main_frame(self):
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5) # 内边距5
        self.sidebar = tk.Frame(main_container, width=100) # 侧边栏宽度100
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10)) # x 侧边距0~10
        edit_area = tk.Frame(main_container)
        edit_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(edit_area)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text = tk.Text(
            edit_area,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set
        )
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) # right 放滚动条
        scrollbar.config(command=self.text.yview) # type: ignore
        self.text.bind('<<Modified>>', self.on_text_modified)
        self.text.edit_modified(False)
        def on_mousewheel(event: Event):
            self.text.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.text.bind("<MouseWheel>", on_mousewheel)
    def on_text_modified(self, event: Optional[Any] = None) -> None:
        if self.text.edit_modified():
            if not self.file_state.is_modified:
                self.file_state.is_modified = True
                self.update_title()
            self.text.edit_modified(False)
    def update_title(self):
        title = "adorable_katze"
        if self.file_state.file_name:
            title = f"{self.file_state.file_name} - {title}"
        if self.file_state.is_modified:
            title = f"* {title}"
        self.root.title(title)
    def Status_bar(self):
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    def run(self):
        # run
        self.root.mainloop()
    def on_closing(self):
        if self.file_state.is_modified:
            save_changes = messagebox.askyesnocancel(
                "Quit",
                "You have unsaved changes. Save before quitting ?"
            )
            if save_changes is None:
                return
            elif save_changes:
                if not self.save():
                    return
        self.root.destroy()
if __name__ == "__main__":
    app = AdorableKatze()
    app.run()
