import requests
import gi

gi.require_version("Gtk","3.0")
from gi.repository import Gtk

class window(Gtk.Window):
    def __init__(self, title="Yuki"):
        Gtk.Window.__init__(self,title = title)
        self.set_size_request(200, 100)
        self.set_border_width(0)
        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.entry = Gtk.Entry()
        self.searchbar = Gtk.Box()
        self.go = Gtk.Button(label='go')
        self.go.connect("clicked",self.getpage)
        self.searchbar.pack_start(self.entry,True,True,0)
        self.searchbar.pack_start(self.go,False,False,0)
        self.grid.attach(self.searchbar,0,0,1,1)
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_hexpand(True)
        self.scroll.set_vexpand(True)
        self.content=Gtk.TextView()
        buff=self.content.get_buffer()
        buff.set_text("will button follow after this? or before this?")
        anch=Gtk.TextChildAnchor()
        self.checkbutton = Gtk.LinkButton(label="testing")
        buff.insert_child_anchor(buff.get_end_iter(),anch)
        self.content.add_child_at_anchor(self.checkbutton,anch)
        #self.content.add(self.checkbutton)
        #buff.set_text("will button follow after this? or before this?")
        self.scroll.add(self.content)
        self.grid.attach(self.scroll,0,1,1,1)

    def getpage(self,button):
        website=self.entry.get_text()
        response = requests.get(website)
        text = response.text
        buff=self.content.get_buffer()
        buff.set_text(text)
        #self.entry.set_text(" ")
        self.content.show()



#class domtree():

win = window()
win.connect("destroy",Gtk.main_quit)
win.show_all()
Gtk.main()