
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty

import os

from datepicker import DatePicker

try:
    from devslib.utils import MessageBoxTime
except:
    os.system("git clone https://github.com/oukiar/devslib")
    from devslib.utils import MessageBoxTime
    
import time


from kivy.core.window import Window
Window.set_icon("pos.png")

class Prestamos(Popup):
    pass
    
class CajaGD(Popup):
    pass

class AddClient(BoxLayout):
    pass

class Ticket(BoxLayout):
    pass

class NoteReg(BoxLayout):
    pass

class Pos(BoxLayout):
    
    def __init__(self, **kwargs):
        super(Pos, self).__init__(**kwargs)
        
        self.cliente = None
    
    def hacerNota(self):
        
        if self.txt_client.text == "":
            MessageBoxTime(title="Ops", size_hint=(None,None), size=(350,120), msg="Por favor especifica el cliente", duration=2).open()
            return
        elif self.cliente == None:
            MessageBoxTime(title="Espere", size_hint=(None,None), size=(350,120), msg="Guardando cliente", duration=2).open()
        
        print "Realizando nota"
        nota = Notas()
        nota.PUser = app.root.user
        nota.Total = self.txt_total.text
        nota.Cliente = self.cliente
        
        products = []
        
        for i in self.lst_note.layout.children:
            print i.txt_producto.text
            
            products.append({
                            "Cantidad":i.txt_cant.text,
                            "Product":i.txt_producto.text,
                            "Precio":i.txt_precio.text,
                            "Total":i.txt_total.text,
                            })
        
        nota.Productos = products
        
        nota.save()
        
        #limpiar controles de nota
        self.lst_note.clear()
        self.lst_note.add_widget(NoteItem() )
        self.txt_client.text = ""
        self.txt_total.text = "0"
        self.img_button.source = "plus.png"
        
        self.cliente = None
        
    def on_completeclient(self, w):
        
        if not hasattr(self, "dropdown"):
            self.dropdown = DropDown()
        
        if len(w.text) > 2:
            
            self.dropdown.clear_widgets()
            
            found = False
            
            for item in app.root.clientes:
                if w.text.upper() in item.Name.upper():
                    but = WhiteButton(text=item.Name, size_hint_y=None, height=40)
                    but.bind(on_press=self.fillClient)
                    but.Cliente = item
                    self.dropdown.add_widget(but)
                    found = True
                    print found
                    
            if found:
                self.dropdown.open(w)
                
                
    def fillClient(self, w):
        
        self.txt_client.text = w.text
        
        self.img_button.source = "ok.png"
        
        self.cliente = w.Cliente
        
        self.dropdown.dismiss()
        
    def addClient(self):
        print "Adding the client: " + self.txt_client.text
        
        self.cliente = Clientes()
        self.cliente.Name = self.txt_client.text
        self.cliente.PUser = app.root.user
        self.cliente.save()
        
        self.img_button.source = "ok.png"
        
    def fillNotas(self):
        print "Llenado lista de notas"
        
        for i in app.root.notas:
            print i
            notareg = NoteReg()
            notareg.txt_fecha.text = str(i.createdAt)
            if i.Cliente != None:
                notareg.txt_cliente.text = i.Cliente.Name
            notareg.txt_total.text = str(i.Total)
            
            self.lst_notas.add_widget(notareg)

class WhiteButton(Button):
    pass

class NoteItem(BoxLayout):
    
    def __init__(self, **kwargs):
        super(NoteItem, self).__init__(**kwargs)
        self.dropdown = DropDown()
    
    def addNoteItem(self, w):
        '''
        inventoryitem = Inventarios()
        inventoryitem.Clave = w.parent.txt_clave.text
        inventoryitem.Producto = w.parent.txt_producto.text
        inventoryitem.Existencias = w.parent.txt_existencias.text
        inventoryitem.Minimo = w.parent.txt_minimo.text
        inventoryitem.Maximo = w.parent.txt_maximo.text
        inventoryitem.Precio = w.parent.txt_precio.text
        inventoryitem.save()
        '''
        
        newitem = NoteItem()
        w.text = "X"
        
        table = app.root.ventas.lst_note
        
        table.add_widget(newitem, index=len(table.layout.children))
        
        app.root.ventas.txt_total.text = str(float(app.root.ventas.txt_total.text) + float(w.parent.txt_total.text))

    def on_completeproduct(self, w):
        print w.text
        if len(w.text) > 2:
            
            self.dropdown.clear_widgets()
            
            for item in app.root.inventarios:
                if w.text.upper() in item.Producto.upper():
                    but = WhiteButton(text=item.Producto, size_hint_y=None, height=40)
                    but.bind(on_press=self.fillProduct)
                    but.Item = item
                    self.dropdown.add_widget(but)
                    
            self.dropdown.open(w)
            
    def fillProduct(self, w):
        
        self.dropdown.dismiss()
        self.txt_producto.text = w.text
        self.txt_precio.text = w.Item.Precio
        if self.txt_cant.text != "":
            self.txt_total.text = str(float(self.txt_cant.text) * float(self.txt_precio.text))

class InventoryItem(BoxLayout):

    def addInventoryItem(self, w):
        inventoryitem = Inventarios()
        inventoryitem.Clave = w.parent.txt_clave.text
        inventoryitem.Producto = w.parent.txt_producto.text
        inventoryitem.Existencias = w.parent.txt_existencias.text
        inventoryitem.Minimo = w.parent.txt_minimo.text
        inventoryitem.Maximo = w.parent.txt_maximo.text
        inventoryitem.Precio = w.parent.txt_precio.text
        inventoryitem.PUser = app.root.user
        
        inventoryitem.save()

        newitem = InventoryItem()
        w.text = "Save"
        
        table = self.parent.parent.parent.parent.lst_inventory
        
        table.add_widget(newitem, index=len(table.layout.children))

class Inventory(BoxLayout):
    lst_inventory = ObjectProperty()

    def fillInventario(self):
        
        print "Llenado inventario"
        
        for i in app.root.inventarios:
            print i
            item = InventoryItem()
            item.btn_action.source = "save.png"
            item.txt_clave.text = str(i.Clave)
            item.txt_producto.text = str(i.Producto)
            item.txt_existencias.text = str(i.Existencias)
            item.txt_minimo.text = str(i.Minimo)
            item.txt_maximo.text = str(i.Maximo)
            item.txt_precio.text = str(i.Precio)
                        
            self.lst_inventory.add_widget(item)

class Main(BoxLayout):
    
    battleplan = ObjectProperty()
    

class DevsHub(FloatLayout):


    def saveClient(self, w):
        
        MessageBoxTime(title="Espere", size_hint=(None,None), size=(350,120), msg="Guardando", duration=2).open()
        
        cliente = Clientes()
        cliente.Name = w.parent.txt_name.text
        cliente.Direccion = w.parent.txt_direccion.text
        cliente.Telefono = w.parent.txt_telefono.text
        cliente.IFE = w.parent.txt_ife.text
        cliente.Monedero = w.parent.txt_monedero.text
        cliente.save()
        
        w.parent.txt_name.text = ""
        w.parent.txt_direccion.text = ""
        w.parent.txt_telefono.text = ""
        w.parent.txt_ife.text = ""
        w.parent.txt_monedero.text = ""
        
        
    def changeTab(self, tabToShow):
        self.main.workSpace.remove_widget(self.currentTab)
        
        self.currentTab = tabToShow
        self.main.workSpace.add_widget(self.currentTab)

    def do_login(self, login):
        print login
        
        try:
            self.user = User.login(login.txt_email.text, login.txt_password.text)
        except:
            self.user = User.signup(login.txt_email.text, login.txt_password.text)
        
        self.remove_widget(login)
        
        self.main = Main()
        self.main.txt_username.text = self.user.username
        self.add_widget(self.main)
        
        self.inventarios = Inventarios.Query.filter(PUser__in=[self.user])
        self.clientes = Clientes.Query.filter(PUser__in=[self.user])
        self.notas = Notas.Query.filter(PUser__in=[self.user])

        #
        self.ventas = Pos()
        self.ventas.fillNotas()
        
        self.inventario = Inventory()
        self.inventario.fillInventario()
        
        self.addclient = AddClient()
        
        self.currentTab = self.ventas

#parse stuff
try:
    Clientes = Object.factory("Clientes")
    Inventarios = Object.factory("Inventarios")
    Notas = Object.factory("Notas")
except:
    from parse_rest.connection import register, ParseBatcher
    from parse_rest.datatypes import Object
    from parse_rest.user import User

    #parse initialization
    register("xIYoHZ0xgLwWIMWzQWPFtxrsZhzmpIQCFCAEJZch", "dqm0KGlhpaK9E0QoGi4dAMWmKuYokiutLegKeRPk")
         
    Clientes = Object.factory("Clientes")
    Inventarios = Object.factory("Inventarios")
    Notas = Object.factory("Notas")

if __name__ == "__main__":
    
    from kivy.app import App
    
    class DevsHubApp(App):
        def build(self):
            return DevsHub()

    #Asi para tener un objeto global y acceder al root widget
    app = DevsHubApp()
    app.run()
