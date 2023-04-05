import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import os.path

_script = sys.argv[0]
_location = os.path.dirname(_script)



_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
_fgcolor = '#000000'  # X11 color: 'black'
_compcolor = 'gray40' # X11 color: #666666
_ana1color = '#c3c3c3' # Closest X11 color: 'gray76'
_ana2color = 'beige' # X11 color: #f5f5dc
_tabfg1 = 'black' 
_tabfg2 = 'black' 
_tabbg1 = 'grey75' 
_tabbg2 = 'grey89' 
_bgmode = 'light' 

_style_code_ran = 0
def _style_code():
    global _style_code_ran
    if _style_code_ran:
       return
    style = ttk.Style()
    if sys.platform == "win32":
       style.theme_use('winnative')
    style.configure('.',background=_bgcolor)
    style.configure('.',foreground=_fgcolor)
    style.configure('.',font='TkDefaultFont')
    style.map('.',background =
       [('selected', _compcolor), ('active',_ana2color)])
    if _bgmode == 'dark':
       style.map('.',foreground =
         [('selected', 'white'), ('active','white')])
    else:
       style.map('.',foreground =
         [('selected', 'black'), ('active','black')])
    style.configure('Vertical.TScrollbar',  background=_bgcolor,
        arrowcolor= _fgcolor)
    style.configure('Horizontal.TScrollbar',  background=_bgcolor,
        arrowcolor= _fgcolor)
    _style_code_ran = 1

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        top.geometry("1536x793+-27+10")
        top.minsize(120, 1)
        top.maxsize(1540, 845)
        top.resizable(1,  1)
        top.title("Toplevel 0")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.top = top

        self.Frame1 = tk.Frame(self.top)
        self.Frame1.place(relx=0.017, rely=0.156, relheight=0.811
                , relwidth=0.975)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(background="#d9d9d9")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="black")
        _style_code()
        self.Scrolledwindow1 = ScrolledWindow(self.Frame1)
        self.Scrolledwindow1.place(relx=0.013, rely=0.171, relheight=0.754
                , relwidth=0.158)
        self.Scrolledwindow1.configure(background="white")
        self.Scrolledwindow1.configure(borderwidth="2")
        self.Scrolledwindow1.configure(highlightbackground="#d9d9d9")
        self.Scrolledwindow1.configure(highlightcolor="black")
        self.Scrolledwindow1.configure(insertbackground="black")
        self.Scrolledwindow1.configure(relief="groove")
        self.Scrolledwindow1.configure(selectbackground="#c4c4c4")
        self.Scrolledwindow1.configure(selectforeground="black")
        self.color = self.Scrolledwindow1.cget("background")
        self.Scrolledwindow1_f = tk.Frame(self.Scrolledwindow1,
                            background=self.color)
        self.Scrolledwindow1.create_window(0, 0, anchor='nw',
                                           window=self.Scrolledwindow1_f)
        self.Scrolledwindow1_1 = ScrolledWindow(self.Frame1)
        self.Scrolledwindow1_1.place(relx=0.174, rely=0.171, relheight=0.754
                , relwidth=0.212)
        self.Scrolledwindow1_1.configure(background="white")
        self.Scrolledwindow1_1.configure(borderwidth="2")
        self.Scrolledwindow1_1.configure(highlightbackground="#d9d9d9")
        self.Scrolledwindow1_1.configure(highlightcolor="black")
        self.Scrolledwindow1_1.configure(insertbackground="black")
        self.Scrolledwindow1_1.configure(relief="groove")
        self.Scrolledwindow1_1.configure(selectbackground="#c4c4c4")
        self.Scrolledwindow1_1.configure(selectforeground="black")
        self.color = self.Scrolledwindow1_1.cget("background")
        self.Scrolledwindow1_1_f = tk.Frame(self.Scrolledwindow1_1,
                            background=self.color)
        self.Scrolledwindow1_1.create_window(0, 0, anchor='nw',
                                           window=self.Scrolledwindow1_1_f)
        self.Frame3 = tk.Frame(self.Frame1)
        self.Frame3.place(relx=0.41, rely=0.011, relheight=0.935, relwidth=0.573)

        self.Frame3.configure(relief='groove')
        self.Frame3.configure(borderwidth="2")
        self.Frame3.configure(relief="groove")
        self.Frame3.configure(background="#d9d9d9")
        self.Frame3.configure(highlightbackground="#d9d9d9")
        self.Frame3.configure(highlightcolor="black")
        self.Scrolledlistbox1 = ScrolledListBox(self.Frame3)
        self.Scrolledlistbox1.place(relx=0.047, rely=0.15, relheight=0.814
                , relwidth=0.283)
        self.Scrolledlistbox1.configure(background="white")
        self.Scrolledlistbox1.configure(cursor="xterm")
        self.Scrolledlistbox1.configure(disabledforeground="#a3a3a3")
        self.Scrolledlistbox1.configure(font="TkFixedFont")
        self.Scrolledlistbox1.configure(foreground="black")
        self.Scrolledlistbox1.configure(highlightbackground="#d9d9d9")
        self.Scrolledlistbox1.configure(highlightcolor="#d9d9d9")
        self.Scrolledlistbox1.configure(selectbackground="#c4c4c4")
        self.Scrolledlistbox1.configure(selectforeground="black")
        self.Scrolledtreeview1 = ScrolledTreeView(self.Frame3)
        self.Scrolledtreeview1.place(relx=0.361, rely=0.15, relheight=0.825
                , relwidth=0.605)
        self.Scrolledtreeview1.configure(columns="Col4 Col2 Col3 Col1")
        # build_treeview_support starting.
        self.Scrolledtreeview1.heading("#0",text="Address")
        self.Scrolledtreeview1.heading("#0",anchor="center")
        self.Scrolledtreeview1.column("#0",width="138")
        self.Scrolledtreeview1.column("#0",minwidth="20")
        self.Scrolledtreeview1.column("#0",stretch="1")
        self.Scrolledtreeview1.column("#0",anchor="center")
        self.Scrolledtreeview1.heading("Col4",text="+0")
        self.Scrolledtreeview1.heading("Col4",anchor="center")
        self.Scrolledtreeview1.column("Col4",width="94")
        self.Scrolledtreeview1.column("Col4",minwidth="30")
        self.Scrolledtreeview1.column("Col4",stretch="1")
        self.Scrolledtreeview1.column("Col4",anchor="w")
        self.Scrolledtreeview1.heading("Col2",text="+1")
        self.Scrolledtreeview1.heading("Col2",anchor="center")
        self.Scrolledtreeview1.column("Col2",width="93")
        self.Scrolledtreeview1.column("Col2",minwidth="20")
        self.Scrolledtreeview1.column("Col2",stretch="1")
        self.Scrolledtreeview1.column("Col2",anchor="w")
        self.Scrolledtreeview1.heading("Col3",text="+2")
        self.Scrolledtreeview1.heading("Col3",anchor="center")
        self.Scrolledtreeview1.column("Col3",width="88")
        self.Scrolledtreeview1.column("Col3",minwidth="20")
        self.Scrolledtreeview1.column("Col3",stretch="1")
        self.Scrolledtreeview1.column("Col3",anchor="w")
        self.Scrolledtreeview1.heading("Col1",text="+3")
        self.Scrolledtreeview1.heading("Col1",anchor="center")
        self.Scrolledtreeview1.column("Col1",width="88")
        self.Scrolledtreeview1.column("Col1",minwidth="30")
        self.Scrolledtreeview1.column("Col1",stretch="1")
        self.Scrolledtreeview1.column("Col1",anchor="w")
        self.Label4 = tk.Label(self.Frame3)
        self.Label4.place(relx=0.058, rely=0.033, height=47, width=213)
        self.Label4.configure(activebackground="#f9f9f9")
        self.Label4.configure(background="#d9d9d9")
        self.Label4.configure(compound='left')
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(highlightbackground="#d9d9d9")
        self.Label4.configure(highlightcolor="black")
        self.Label4.configure(text='''Registers''')
        self.Label5 = tk.Label(self.Frame3)
        self.Label5.place(relx=0.361, rely=0.05, height=41, width=485)
        self.Label5.configure(activebackground="#f9f9f9")
        self.Label5.configure(background="#d9d9d9")
        self.Label5.configure(compound='left')
        self.Label5.configure(disabledforeground="#a3a3a3")
        self.Label5.configure(foreground="#000000")
        self.Label5.configure(highlightbackground="#d9d9d9")
        self.Label5.configure(highlightcolor="black")
        self.Label5.configure(text='''Memory''')
        self.Labelframe1 = tk.LabelFrame(self.Frame1)
        self.Labelframe1.place(relx=0.014, rely=0.0, relheight=0.151
                , relwidth=0.374)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(foreground="#000000")
        self.Labelframe1.configure(text='''Console''')
        self.Labelframe1.configure(background="#d9d9d9")
        self.Labelframe1.configure(highlightbackground="#d9d9d9")
        self.Labelframe1.configure(highlightcolor="black")
        self.Label2 = tk.Label(self.Labelframe1)
        self.Label2.place(relx=0.018, rely=0.309, height=45, width=203
                , bordermode='ignore')
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(compound='left')
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''PC''')
        self.Label3 = tk.Label(self.Labelframe1)
        self.Label3.place(relx=0.5, rely=0.309, height=45, width=246
                , bordermode='ignore')
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(compound='left')
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(highlightbackground="#d9d9d9")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''Machine Code''')
        self.Frame2 = tk.Frame(self.top)
        self.Frame2.place(relx=0.017, rely=0.044, relheight=0.1, relwidth=0.975)
        self.Frame2.configure(relief='groove')
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(relief="groove")
        self.Frame2.configure(background="#d9d9d9")
        self.Frame2.configure(highlightbackground="#d9d9d9")
        self.Frame2.configure(highlightcolor="black")
        self.Label1 = tk.Label(self.Frame2)
        self.Label1.place(relx=0.034, rely=0.228, height=36, width=726)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(anchor='w')
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(compound='left')
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="#808080")
        self.Label1.configure(text='''RISCV Simulator : Group 16''')
        self.Button1 = tk.Button(self.Frame2)
        self.Button1.place(relx=0.868, rely=0.38, height=24, width=157)
        self.Button1.configure(activebackground="beige")
        self.Button1.configure(activeforeground="black")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(compound='left')
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Simulate''')

# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''
    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        # Copy geometry methods of master  (taken from ScrolledText.py)
        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledListBox(AutoScroll, tk.Listbox):
    '''A standard Tkinter Listbox widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)
    def size_(self):
        sz = tk.Listbox.size(self)
        return sz

class ScrolledWindow(AutoScroll, tk.Canvas):
    '''A standard Tkinter Canvas widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Canvas.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

class ScrolledTreeView(AutoScroll, ttk.Treeview):
    '''A standard ttk Treeview widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')
# def start_up():
#     gui_support.main()

if __name__ == '__main__':
    global root, gui, t1, t2
    root = tk.Tk()
    gui  = Toplevel1(root)
    root.mainloop()



