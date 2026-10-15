import tkinter          #GUI, including file manager
import ttkbootstrap     #bootstrap styling for the GUI
import subprocess, sys  #executing python code
import re               #regular expression

patterns = {
    "keywords": r'\b(def|class|if|else|elif|for|while|in|import|from|\
        return|True|False|None|and|or|not|try|except|with|as|print)\b',
    "strings": r'(["\'])(?:\\.|(?!\1).)*\1',
    "comments": r'#.*'
}

#in tkinter editor, 1.0 = start (first line)
def highlight(event=None):
    text = editor.get("1.0", "end")
    for tag in ("keywords", "strings", "comments"):
        editor.tag_remove(tag, "1.0", "end")

    for tag, pattern in patterns.items():
        for m in re.finditer(pattern, text): #list of pattern matches
            editor.tag_add(tag, f"1.0+{m.start()}c", f"1.0+{m.end()}c")

def run():
    process = subprocess.run(
        [
            sys.executable,  # uses the Python interpreter running this application
            "-c",  # tells Python to execute the following string as code
            editor.get("1.0", "end")  # retrieves all code from the editor
        ],
        capture_output = True,  # captures standard output and standard error
        text = True  # returns captured output as strings rather than bytes
    )
    console.insert("end", process.stdout + process.stderr)

def open_file():
    file_path = tkinter.filedialog.askopenfilename(filetypes=[("Python", "*.py")])
    if file_path:
        editor.delete("1.0", "end")
        editor.insert("1.0", open(file_path, encoding="utf-8").read())
        highlight()

def save_file():
    file_path = tkinter.filedialog.asksaveasfilename(
        defaultextension=".py", filetypes=[("Python", "*.py")])
    if file_path:
        open(file_path, "w", encoding="utf-8").write(editor.get("1.0", "end"))

window = ttkbootstrap.Window(themename="darkly") #equivalent of tkinter.Tk()
window.title("Python Editor")

menubar = ttkbootstrap.Frame(window)
menubar.pack(fill="x") #stretch menubar horizontally

ttkbootstrap.Button(menubar, text="▶ Run", command=run).pack(side="left")
ttkbootstrap.Button(menubar, text="📄 Open", command=open_file).pack(side="left")
ttkbootstrap.Button(menubar, text="💾 Save", command=save_file).pack(side="left")

panedwindow = tkinter.PanedWindow(window, orient="vertical", bg="#333333", sashwidth=5) #sashwidth = divider width
panedwindow.pack(fill="both", expand=True)

editor = tkinter.Text(panedwindow, bg="#1e1e1e", fg="#d4d4d4", 
                 insertbackground="#d4d4d4", font=("Consolas", 12), undo=True)

console = tkinter.Text(panedwindow, bg="#111111", fg="#dddddd", 
                  font=("Consolas", 12), height=10)

editor.insert("1.0", 'print("Hello, world!")')
highlight()

panedwindow.add(editor)
panedwindow.add(console)

editor.tag_configure("keywords", foreground="#569cd6")
editor.tag_configure("strings", foreground="#ce9178")
editor.tag_configure("comments", foreground="#6a9955")
editor.bind("<KeyRelease>", highlight)

window.mainloop()
