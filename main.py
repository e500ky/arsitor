from customtkinter import *
from tkinter import *
from tkinter import font
import os, json

set_appearance_mode("system")

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Arsitor")
        self.geometry("800x600")
        self.minsize(800, 600)
        self.iconbitmap("assets/icon.ico", default="assets/icon.ico")

        self.filepath = None
        self.settings = self.loadSettings()
        
        self.setGUI()

    def setGUI(self):
        self.setWrAr()
        self.bottomArea()
        self.applySettings()
        self.checkFilePath()

    def checkFilePath(self):
        if self.filepath is not None:
            saveState = self.checkSaveState()
            self.title(f"Arsitor - {self.filepath} {saveState}")
        self.after(100, self.checkFilePath)

    def checkSaveState(self):
        if self.filepath is not None:
            with open(self.filepath, 'r', encoding="utf-8") as file:
                content = file.read()
            return "*" if self.writableArea.get(1.0, END) != content else ""

    def setWrAr(self):
        self.writableArea = CTkTextbox(self, font=(self.settings["font_family"], self.settings["font_size"]), wrap=WORD, corner_radius=self.settings["corner_radius"], border_spacing=20)
        self.writableArea.pack(fill=BOTH, expand=True, padx=self.settings["border_space"], pady=self.settings["border_space"])
        font_measure = font.Font(font=self.writableArea.cget("font")).measure(" " * self.settings["tab_size"])
        self.writableArea._textbox.config(selectbackground="#666", selectforeground="white", tabs=font_measure)
        self.writableArea.focus()

        self.writableArea.bind("<Control-s>", lambda event: self.saveFile())
        self.writableArea.bind("<Control-Shift-S>", lambda event: self.saveFileAs())
        self.writableArea.bind("<Control-o>", lambda event: self.openFile())
        self.writableArea.bind("<F1>", lambda event: self.openSettings())
        self.writableArea.bind("<Alt-s>", lambda event: self.openSettings())
    
    def bottomArea(self):
        self.bottomFrame = CTkFrame(self, height=30, corner_radius=0, fg_color=self.settings["bottom_frame_color"])
        self.bottomFrame.pack(fill=X, side=BOTTOM)

        self.openButton = self.createButton(self.bottomFrame, "📂 Open", self.openFile, LEFT)
        self.saveButton = self.createButton(self.bottomFrame, "💾 Save", self.saveFile, LEFT)
        self.saveAsButton = self.createButton(self.bottomFrame, "💾 Save As", self.saveFileAs, LEFT)

        self.encodingLabel = CTkLabel(self.bottomFrame, text="UTF-8", anchor="w", fg_color="gray17", text_color="white")
        self.encodingLabel.pack(side=RIGHT, padx=10)

        self.positionLabel = CTkLabel(self.bottomFrame, text="Ln 1, Col 1", anchor="w", fg_color="gray17", text_color="white")
        self.positionLabel.pack(side=RIGHT, padx=10)

        self.selectionLabel = CTkLabel(self.bottomFrame, text="0 Chars Selected", anchor="w", fg_color="gray17", text_color="white")
        self.selectionLabel.pack(side=RIGHT, padx=10)

        self.runButton = CTkButton(self.bottomFrame, text="Run", font=("Segoe UI Emoji", 15), command=self.runFile, text_color_disabled="#f0f0f0", corner_radius=0, fg_color="gray17", hover_color="gray20")
        self.runButton.pack(side=LEFT, padx=0, pady=0)
        self.runButton.pack_forget()  # Initially hide the Run button

        self.createButton(self.bottomFrame, "⚙️ Settings", self.openSettings, RIGHT)
        
        self.writableArea.bind("<F5>", lambda event: self.runFile())
        self.writableArea.bind("<KeyRelease>", self.checkExecutable)
        self.writableArea.bind("<ButtonRelease>", self.checkExecutable)
        self.writableArea.bind("<KeyRelease>", self.updateStatus)
        self.writableArea.bind("<ButtonRelease>", self.updateStatus)

    def createButton(self, parent, text, command, side):
        button = CTkButton(parent, text=text, font=("Segoe UI Emoji", 15), command=command, text_color_disabled="#f0f0f0", corner_radius=0, fg_color="gray17", hover_color="gray20")
        button.pack(side=side, padx=0, pady=0)

    def checkExecutable(self, event=None):
        if self.filepath and os.access(self.filepath, os.X_OK):
            self.runButton.pack(side=LEFT, padx=0, pady=0)
        else:
            self.runButton.pack_forget()

    def runFile(self):
        if self.filepath and self.runButton.winfo_ismapped():
            os.startfile(self.filepath)

    def updateStatus(self, event=None):
        row, col = self.writableArea.index("insert").split(".")
        row, col = int(row), int(col) + 1
        selected = self.writableArea.tag_ranges("sel")
        selected_chars = len(self.writableArea.get(*selected)) if selected else 0
        self.positionLabel.configure(text=f"Ln {row}, Col {col}")
        self.selectionLabel.configure(text=f"{selected_chars} Chars Selected")

    def openFile(self):
        self.fp = self.filepath
        self.filepath = filedialog.askopenfilename()
        if self.filepath:
            with open(self.filepath, 'r', encoding="utf-8") as file:
                content = file.read()
            self.writableArea.delete(1.0, END)
            self.writableArea.insert(INSERT, content)
            self.checkExecutable()
        else:
            self.filepath = self.fp

    def saveFile(self):
        if self.filepath:
            with open(self.filepath, 'w', encoding="utf-8") as file:
                content = self.writableArea.get(1.0, END)
                file.write(content)
            self.saveButton.configure(text="💾 Saved", state=DISABLED)
            self.saveButton.after(1000, lambda: self.saveButton.configure(text="💾 Save", state=NORMAL))
            self.checkExecutable()
        else:
            self.saveFileAs()

    def saveFileAs(self):
        self.fp = self.filepath
        self.filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if self.filepath:
            with open(self.filepath, 'w', encoding="utf-8") as file:
                content = self.writableArea.get(1.0, END)
                file.write(content)
            self.saveAsButton.configure(text="💾 Saved As", state=DISABLED)
            self.saveAsButton.after(1000, lambda: self.saveAsButton.configure(text="💾 Save As", state=NORMAL))
            self.checkExecutable()
        else:
            self.filepath = self.fp

    def openSettings(self):
        self.settingsWindow = CTkToplevel(self)
        self.settingsWindow.wm_iconbitmap("assets/icon.ico")
        self.settingsWindow.title("Arsitor - Settings")
        self.settingsWindow.geometry("355x445")
        self.settingsWindow.resizable(False, False)
        self.settingsWindow.attributes("-topmost", True)
        self.settingsWindow.after(100, lambda: (self.settingsWindow.attributes("-topmost", False), self.settingsWindow.focus()))

        settingsFrame = CTkFrame(self.settingsWindow)
        settingsFrame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        self.themeOption = self.createSettingsRow(settingsFrame, "Theme Mode:", 0, CTkOptionMenu, ["Light", "Dark", "System"], self.settings["theme_mode"], self.changeTheme)
        self.fontSizeEntry = self.createSettingsRow(settingsFrame, "Font Size:", 1, CTkEntry, None, self.settings["font_size"])
        self.fontFamilyEntry = self.createSettingsRow(settingsFrame, "Font Family:", 3, CTkEntry, None, self.settings["font_family"])
        self.tabSizeEntry = self.createSettingsRow(settingsFrame, "Tab Size:", 2, CTkEntry, None, self.settings["tab_size"])
        self.borderSpaceEntry = self.createSettingsRow(settingsFrame, "Border Space:", 4, CTkEntry, None, self.settings["border_space"])
        self.cornerRadiusEntry = self.createSettingsRow(settingsFrame, "Corner Radius:", 5, CTkEntry, None, self.settings["corner_radius"])

        self.saveButton = CTkButton(settingsFrame, text="Save", text_color_disabled="white", command=lambda: self.saveSettings(
            self.themeOption.get(), self.fontSizeEntry.get(), self.tabSizeEntry.get(), self.fontFamilyEntry.get(), self.borderSpaceEntry.get(), self.cornerRadiusEntry.get()))
        self.saveButton.grid(row=6, column=0, columnspan=2, pady=(40, 0))

        resetButton = CTkButton(settingsFrame, text="Reset to Default", text_color=self.cornerRadiusEntry.cget("text_color"), command=self.resetSettings, fg_color=settingsFrame.cget("fg_color"), bg_color=settingsFrame.cget("fg_color"), hover=False)
        resetButton.grid(row=7, column=0, columnspan=2, pady=(10, 0))

    def createSettingsRow(self, parent, label_text, row, widget_class, values, default_value, command=None):
        label = CTkLabel(parent, text=label_text, font=("Sans Serif", 16))
        label.grid(row=row, column=0, padx=20, pady=10, sticky="w")
        widget = widget_class(parent, values=values, command=command) if values else widget_class(parent)
        widget.insert(0, str(default_value)) if not values else widget.set(default_value)
        widget.grid(row=row, column=1, padx=20, pady=10, sticky="e")
        setattr(self, f"{label_text.replace(' ', '').replace(':', '').lower()}Entry", widget)

        return widget

    def resetSettings(self):
        default_settings = {
            "theme_mode": "System",
            "font_size": 20,
            "tab_size": 4,
            "font_family": "Candara",
            "bottom_frame_color": "gray17",
            "border_space": 7.5,
            "corner_radius": 10
        }
        with open("settings.json", "w") as settings_file:
            json.dump(default_settings, settings_file, indent=4, ensure_ascii=False)
        self.settings = default_settings
        self.applySettings()
        self.settingsWindow.destroy()

    def changeTheme(self, mode):
        set_appearance_mode(mode)

    def saveSettings(self, theme_mode, font_size, tab_size, font_family, border_space, corner_radius):
        self.saveButton.configure(text="Saved", state=DISABLED)
        self.saveButton.after(1000, lambda: self.saveButton.configure(text="Save", state=NORMAL))
        self.settings.update({
            "theme_mode": theme_mode,
            "font_size": int(font_size),
            "tab_size": int(tab_size),
            "font_family": font_family,
            "border_space": float(border_space),
            "corner_radius": float(corner_radius)
        })
        with open("settings.json", "w") as settings_file:
            json.dump(self.settings, settings_file)
        self.applySettings()
        self.settingsWindow.destroy()

    def loadSettings(self):
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as settings_file:
                return json.load(settings_file)
        else:
            default = {
                "theme_mode": "System",
                "font_size": 20,
                "font_family": "Candara",
                "tab_size": 4,
                "border_space": 7.5,
                "bottom_frame_color": "gray17",
                "corner_radius": 10
            }
            with open("settings.json", "w") as settings_file:
                json.dump(default, settings_file, indent=4, ensure_ascii=False)
            return default

    def applySettings(self):
        self.writableArea.configure(font=(self.settings["font_family"], self.settings["font_size"]), corner_radius=self.settings["corner_radius"], tabs=' ' * self.settings["tab_size"])
        set_appearance_mode(self.settings["theme_mode"])
        self.bottomFrame.configure(fg_color=self.settings["bottom_frame_color"])
        self.writableArea.pack(padx=self.settings["border_space"], pady=self.settings["border_space"], fill=BOTH, expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()