import tkinter as tk
from tkinter import filedialog, messagebox, font, colorchooser

class PixelParchment:
    def __init__(self, root):
        self.root = root
        self.file_path = None
        self.text_widget = None
        self.current_font_family = None
        self.current_font_size = 12
        self.current_text_color = "black"
        self.current_bg_color = "white"
        self.text_modified = False
        self.undo_stack = []
        self.redo_stack = []
        self.setup_gui()

    def setup_gui(self):
        self.root.title("PixelParchment")
        self.root.geometry("800x600")

        # Create Menu
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_file_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_application, accelerator="Ctrl+Q")
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Cut", command=self.cut_text, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy_text, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste_text, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Undo", command=self.undo_text, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo_text, accelerator="Ctrl+Y")
        menubar.add_cascade(label="Edit", menu=edit_menu)

        format_menu = tk.Menu(menubar, tearoff=0)
        self.font_menu = tk.Menu(format_menu, tearoff=0)
        format_menu.add_cascade(label="Font", menu=self.font_menu)
        format_menu.add_command(label="Change Font", command=self.change_font)
        format_menu.add_separator()
        format_menu.add_command(label="Text Color", command=self.change_text_color)
        format_menu.add_command(label="Background Color", command=self.change_bg_color)
        menubar.add_cascade(label="Format", menu=format_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Increase Font Size", command=self.increase_font_size, accelerator="Ctrl++")
        view_menu.add_command(label="Decrease Font Size", command=self.decrease_font_size, accelerator="Ctrl+-")
        menubar.add_cascade(label="View", menu=view_menu)

        fun_menu = tk.Menu(menubar, tearoff=0)
        fun_menu.add_command(label="Count Words", command=self.count_words, accelerator="Ctrl+W")
        fun_menu.add_command(label="Highlight Selection", command=self.highlight_selection, accelerator="Ctrl+H")
        menubar.add_cascade(label="Fun", menu=fun_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="How to Use", command=self.show_help_dialog)
        help_menu.add_command(label="About", command=self.show_about_dialog)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

        # Create Text Widget
        self.text_widget = tk.Text(self.root, wrap="word", font=("Arial", 12))
        self.text_widget.pack(fill="both", expand=True)

        # Bind Keyboard Shortcuts
        self.root.bind("<Control-n>", lambda event: self.new_file())
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-S>", lambda event: self.save_file_as())
        self.root.bind("<Control-q>", lambda event: self.exit_application())
        self.root.bind("<Control-x>", lambda event: self.cut_text())
        self.root.bind("<Control-c>", lambda event: self.copy_text())
        self.root.bind("<Control-v>", lambda event: self.paste_text())
        self.root.bind("<Control-z>", lambda event: self.undo_text())
        self.root.bind("<Control-y>", lambda event: self.redo_text())
        self.root.bind("<Control-plus>", lambda event: self.increase_font_size())
        self.root.bind("<Control-minus>", lambda event: self.decrease_font_size())
        self.root.bind("<Control-w>", lambda event: self.count_words())
        self.root.bind("<Control-h>", lambda event: self.highlight_selection())
        self.text_widget.bind("<Key>", self.mark_text_as_modified)

        # Load default font families
        self.available_fonts = font.families()
        self.load_default_fonts()

    def load_default_fonts(self):
        default_fonts = ["Arial", "Courier New", "Times New Roman", "Verdana"]
        for font_family in default_fonts:
            self.font_menu.add_command(label=font_family, command=lambda family=font_family: self.set_font(family))

    def set_font(self, font_family):
        self.current_font_family = font_family
        self.text_widget.configure(font=(self.current_font_family, self.current_font_size))

    def change_font(self):
        font_chooser = tk.Toplevel(self.root)
        font_chooser.title("Choose Font")

        label = tk.Label(font_chooser, text="Select Font Family:", font=("Arial", 12))
        label.pack(padx=10, pady=10)

        font_family_var = tk.StringVar(font_chooser)
        font_family_var.set(self.current_font_family if self.current_font_family else "")
        font_family_dropdown = tk.OptionMenu(font_chooser, font_family_var, *self.available_fonts)
        font_family_dropdown.config(font=("Arial", 12))
        font_family_dropdown.pack(padx=10, pady=5)

        apply_button = tk.Button(font_chooser, text="Apply", command=lambda: self.apply_font(font_family_var.get()), font=("Arial", 12))
        apply_button.pack(pady=10)

    def apply_font(self, font_family):
        if font_family:
            self.current_font_family = font_family
            self.text_widget.configure(font=(self.current_font_family, self.current_font_size))

    def change_text_color(self):
        color = colorchooser.askcolor(title="Choose Text Color")
        if color:
            self.current_text_color = color[1]
            self.text_widget.config(fg=self.current_text_color)

    def change_bg_color(self):
        color = colorchooser.askcolor(title="Choose Background Color")
        if color:
            self.current_bg_color = color[1]
            self.text_widget.config(bg=self.current_bg_color)

    def increase_font_size(self):
        self.current_font_size += 2
        self.text_widget.configure(font=(self.current_font_family, self.current_font_size))

    def decrease_font_size(self):
        if self.current_font_size > 2:
            self.current_font_size -= 2
            self.text_widget.configure(font=(self.current_font_family, self.current_font_size))

    def new_file(self):
        if self.file_path:
            save_prompt = messagebox.askyesnocancel("Save Changes", "Save changes to the current file?")
            if save_prompt is None:
                return
            elif save_prompt:
                self.save_file()

        self.file_path = None
        self.text_widget.delete("1.0", tk.END)
        self.text_modified = False
        self.update_window_title()

    def open_file(self):
        if self.file_path:
            save_prompt = messagebox.askyesnocancel("Save Changes", "Save changes to the current file?")
            if save_prompt is None:
                return
            elif save_prompt:
                self.save_file()

        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    self.text_widget.delete("1.0", tk.END)
                    self.text_widget.insert(tk.END, file.read())
                    self.file_path = file_path
                    self.text_modified = False
                    self.update_window_title()
            except FileNotFoundError:
                messagebox.showerror("Error", "File not found.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while opening the file:\n{str(e)}")

    def save_file(self):
        if self.file_path:
            try:
                with open(self.file_path, "w") as file:
                    file.write(self.text_widget.get("1.0", tk.END))
                    self.text_modified = False
                    self.update_window_title()
                    messagebox.showinfo("Saved", f"File saved: {self.file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the file:\n{str(e)}")
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.text_widget.get("1.0", tk.END))
                    self.file_path = file_path
                    self.text_modified = False
                    self.update_window_title()
                    messagebox.showinfo("Saved", f"File saved: {self.file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the file:\n{str(e)}")

    def exit_application(self):
        if self.file_path:
            save_prompt = messagebox.askyesnocancel("Save Changes", "Save changes to the current file?")
            if save_prompt is None:
                return
            elif save_prompt:
                self.save_file()

        self.root.destroy()

    def cut_text(self):
        try:
            self.text_widget.event_generate("<<Cut>>")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while cutting the text:\n{str(e)}")

    def copy_text(self):
        try:
            self.text_widget.event_generate("<<Copy>>")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while copying the text:\n{str(e)}")

    def paste_text(self):
        try:
            self.text_widget.event_generate("<<Paste>>")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while pasting the text:\n{str(e)}")

    def undo_text(self):
        try:
            if self.undo_stack:
                text = self.undo_stack.pop()
                self.redo_stack.append(self.text_widget.get("1.0", tk.END))
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert(tk.END, text)
                self.text_modified = True
                self.update_window_title()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while undoing the text:\n{str(e)}")

    def redo_text(self):
        try:
            if self.redo_stack:
                text = self.redo_stack.pop()
                self.undo_stack.append(self.text_widget.get("1.0", tk.END))
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert(tk.END, text)
                self.text_modified = True
                self.update_window_title()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while redoing the text:\n{str(e)}")

    def mark_text_as_modified(self, event):
        self.text_modified = True
        self.update_window_title()

    def count_words(self):
        text = self.text_widget.get("1.0", tk.END)
        words = text.split()
        word_count = len(words)
        messagebox.showinfo("Word Count", f"Total words: {word_count}")

    def highlight_selection(self):
        if self.text_widget.tag_ranges("sel"):
            self.text_widget.tag_config("highlight", background="yellow")
            self.text_widget.tag_add("highlight", "sel.first", "sel.last")
        else:
            messagebox.showinfo("No Selection", "Please select some text to highlight.")

    def update_window_title(self):
        title = "PixelParchment"
        if self.file_path:
            title += f" - {self.file_path}"
        if self.text_modified:
            title += " *"
        self.root.title(title)

    def show_help_dialog(self):
        help_text = """
        How to Use PixelParchment:
        
        - New File: Create a new empty file.
        - Open: Open an existing text file.
        - Save: Save the current file.
        - Save As: Save the current file with a different name or location.
        - Exit: Exit the PixelParchment application.
        
        - Cut: Cut the selected text.
        - Copy: Copy the selected text.
        - Paste: Paste the copied or cut text.
        - Undo: Undo the last edit.
        - Redo: Redo the previously undone edit.
        
        - Font: Select a font for the text.
        - Change Font: Open a font selection dialog to change the font.
        
        - Increase Font Size: Increase the size of the font.
        - Decrease Font Size: Decrease the size of the font.
        
        - Text Color: Change the color of the text.
        - Background Color: Change the background color.
        
        - Count Words: Count the number of words in the text.
        - Highlight Selection: Highlight the selected text.
        
        Note: Keyboard shortcuts are available for many actions. They are displayed in the menus.
        """
        messagebox.showinfo("How to Use PixelParchment", help_text)

    def show_about_dialog(self):
        about_text = "PixelParchment is a stylish and versatile text editor designed for your writing needs."
        messagebox.showinfo("About PixelParchment", about_text)

    def run(self):
        self.root.mainloop()

root = tk.Tk()
notepad = PixelParchment(root)
notepad.run()
