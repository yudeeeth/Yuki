import requests
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk

def req(str):
    r = requests.get(str)
    return r.text

# class render():
#     def __init__(self,obj)

class window(Gtk.Window):
    def __init__(self, title="Yuki"):
        Gtk.Window.__init__(self,title = title)
        self.set_size_request(200, 100)
        self.set_border_width(0)
        self.notebook = note()
        self.add(self.notebook)
        self.connect("destroy",Gtk.main_quit)
        self.show_all()

class note(Gtk.Notebook):
    def __init__(self):
        Gtk.Notebook.__init__(self)
        #self.plus = Gtk.Box()
        self.pages=1
        self.tomorrowpage = page()
        self.buttonfortomorrow = Gtk.Button(label="+")
        self.buttonfortomorrow.connect("clicked",self.addpage)
        self.mainpage()
        self.pluspage()


    def mainpage(self):
        #setting up the tabname on top for each new tab
        firstpage = page()
        logo = Gtk.HBox()
        label = Gtk.Label(label = "New tab")
        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU)
        close_button = Gtk.Button()
        close_button.set_image(image)
        close_button.set_relief(Gtk.ReliefStyle.NONE)
        close_button.connect("clicked",self.delpage,firstpage)
        logo.pack_start(label,True,True,0)
        logo.pack_end(close_button,False,False,0)
        logo.show_all()
        self.append_page(firstpage,logo)
        
    def pluspage(self):
        self.append_page(self.tomorrowpage,self.buttonfortomorrow)
        self.show_all()

    def addpage(self,button):
        self.remove(self.tomorrowpage)
        self.mainpage()
        self.pages +=1
        if self.pages<10:
            self.pluspage()
        self.show_all()


    def delpage(self,button,page):
        self.remove(page)
        self.pages -= 1
        if self.pages==9:
            self.pluspage()
        self.show_all()
        if self.pages == 0:
            Gtk.main_quit()



class page(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.topmenu = Gtk.Box()
        self.backbtn = Gtk.Button(label="<")
        self.nextbtn = Gtk.Button(label=">")
        self.refresh = Gtk.Button(label="H")
        self.bar = Gtk.SearchEntry()
        self.bar.connect("activate",self.handlepage)
        self.settings = Gtk.Button(label="S")
        self.topmenu.pack_start(self.backbtn,False,False,0)
        self.topmenu.pack_start(self.nextbtn,False,False,0)
        self.topmenu.pack_start(self.refresh,False,False,0)
        self.topmenu.pack_start(self.bar,True,True,0)
        self.topmenu.pack_start(self.settings,False,False,0)

        self.document = Gtk.ScrolledWindow()
        self.document.set_hexpand(True)
        self.document.set_vexpand(True)
        self.attach(self.topmenu,0,0,1,1)
        self.attach(self.document,0,1,1,1)

    def handlepage(self,bar):
        self.website = req(self.bar.get_text())
        self.content = Gtk.TextView()
        buff = self.content.get_buffer()
        buff.set_text(self.website)
        self.document.add(self.content)
        self.show_all()


win = window()
Gtk.main()
