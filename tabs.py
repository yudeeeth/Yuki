from bs4 import BeautifulSoup as bs
# soup = BeautifulSoup(html_doc, 'html.parser')
import requests
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk

def listToString(s):  
    str1 = " "
    return (str1.join(s)) 

def req(str,page):
    r = requests.get(str)
    t = tree(r.text,page)
    # t.construct(t.soup,t.doc)
    # show(t.doc)
    #0return r.text

class render():
    def __init__(self,tree):
        pass

class node():
    def __init__(self,parent):
        self.parent = parent
        self.name  = "html"
        self.children = []
        self.terminal = 0
        self.element = Gtk.TextView()
        self.buffer = self.element.get_buffer()
        self.buffer.set_text("basic")

def show(node):
    try:
        node.element.show_all()
        print( f"name: {type(node.element)} + {node.element} {node.children[0].element}")
    except:
        node.element.show_all()
        print( f"name: {type(node.element)} + {node.element}")
    try:
        for i in node.children:
            show(i)
    except:
        pass

class tree():
    def __init__(self,html,page):
        #make into bs object
        self.count = 0
        self.soup = bs(html,"html.parser")
        self.soup = self.soup.html
        self.html = html
        self.doc = node(0)
        self.doc.element = page
        self.construct(self.soup,self.doc)
        show(self.doc)

    def construct(self,bs,n):
        #if bs.contents == 
        
        if bs.name == None:
            n.name = "string"
            
            # for i in bs.contents:
            #     n.element += i

        else:
            n.name = bs.name
        #print(n.name)
        if n.name == "html" or n.name == "head" or n.name == "body" or n.name == "div" or n.name == "form":
            n.element = Gtk.Box(Gtk.Orientation(1))
            print("made" + n.name)
            n.element.show_all()
            if n.parent != 0:
                n.parent.element.add(n.element)
                n.element.show_all()

            # else:
            #     n.parent.add(n.element)
            #     self.count+=1
            #     n.parent.show_all()
            for i in bs.children:
                n.children.append(node(n))
                self.construct(i,n.children[-1])
        if n.name == "a":
            n.terminal=1
            n.element = Gtk.LinkButton(label = listToString(bs.contents))
        elif n.name == "button":
            n.terminal=1
            n.element = Gtk.Button(label = listToString(bs.contents))
        elif n.name == "string":
            n.element = Gtk.TextView()
            buffer = n.element.get_buffer()
            buffer.set_text(listToString(bs.contents))
            n.terminal = 1
        elif n.name == "p":
            n.element = Gtk.TextView()
            temp = n.element.get_buffer()
            temp.set_text(listToString(bs.contents))
    def getdoc(self):
        return self.doc

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
        self.show_all()


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
        self.max = 0
        self.pagesback = []
        self.pagesnext = []
        self.pageindex = -1
        self.topmenu = Gtk.Box()
        self.backbtn = Gtk.Button(label="<")
        self.backbtn.connect("clicked",self.goback)
        self.nextbtn = Gtk.Button(label=">")
        self.nextbtn.connect("clicked",self.gonext)
        self.refresh = Gtk.Button(label="H")
        self.bar = Gtk.SearchEntry()
        self.bar.connect("activate",self.handlepage)
        self.settings = Gtk.Button(label="S")
        self.topmenu.pack_start(self.backbtn,False,False,0)
        self.topmenu.pack_start(self.nextbtn,False,False,0)
        self.topmenu.pack_start(self.refresh,False,False,0)
        self.topmenu.pack_start(self.bar,True,True,0)
        self.topmenu.pack_start(self.settings,False,False,0)
        self.scroll = Gtk.ScrolledWindow()
        self.document = Gtk.Box()
        self.scroll.add(self.document)
        self.scroll.set_hexpand(True)
        self.scroll.set_vexpand(True)
        self.attach(self.topmenu,0,0,1,1)
        self.attach(self.scroll,0,1,1,1)

        # self.content = Gtk.TextView()

    def handlepage(self,bar):
        self.pagesback.append(self.bar.get_text())
        self.pageindex+=1
        self.max=self.pageindex
        try:
            while self.pagesnext[0]!=None:
                self.pagesnext.pop()
        except:
            pass
        req(self.bar.get_text(),self.document)
        # buff = self.content.get_buffer()
        # buff.set_text(self.website)
        self.show_all()
        self.document.show_all()



    def goback(self,button):
        if self.pageindex >0:
            self.pageindex-=1
            self.pagesnext.append(self.pagesback.pop())
            req(self.pagesback[self.pageindex],self.document)
            # buff = self.content.get_buffer()
            # buff.set_text(self.website)
            self.show_all()

    def gonext(self,button):
        if self.pageindex<self.max:
            self.pageindex+=1
            self.pagesback.append(self.pagesnext.pop())
            req(self.pagesback[self.pageindex],self.document)
            self.show_all()

win = window()
Gtk.main()
