
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

from kivy.properties import ObjectProperty, StringProperty

from datepicker import DatePicker

import time

#parse stuff
from parse_rest.connection import register, ParseBatcher
from parse_rest.datatypes import Object
from parse_rest.user import User

#parse initialization
register("xIYoHZ0xgLwWIMWzQWPFtxrsZhzmpIQCFCAEJZch", "dqm0KGlhpaK9E0QoGi4dAMWmKuYokiutLegKeRPk")
     
Clientes = Object.factory("Clientes")
Inventarios = Object.factory("Inventarios")
Notas = Object.factory("Notas")

class AddClient(BoxLayout):
    pass

class Ticket(BoxLayout):
    pass

class Pos(BoxLayout):
    def hacerNota(self):
        print "Realizando nota"
        nota = Notas()
        nota.PUser = devshub.root.user
        nota.Total = self.txt_total.text
        
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
        
        
    def on_completeclient(self, w):
        
        if not hasattr(self, "dropdown"):
            self.dropdown = DropDown()
        
        if len(w.text) > 2:
            
            self.dropdown.clear_widgets()
            
            found = False
            
            for item in devshub.root.clientes:
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
        
        self.dropdown.dismiss()
        self.txt_client.text = w.text
        
        self.img_button.source = "ok.png"
        
        self.cliente = w.Cliente
        
    def addClient(self):
        print "Adding the client: " + self.txt_client.text
        
        self.cliente = Clientes()
        self.cliente.Name = self.txt_client.text
        self.cliente.PUser = devshub.root.user
        self.cliente.save()
        
        self.img_button.source = "ok.png"

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
        
        table = devshub.root.main.ventas.lst_note
        
        table.add_widget(newitem, index=len(table.layout.children))
        
        devshub.root.main.ventas.txt_total.text = str(float(devshub.root.main.ventas.txt_total.text) + float(w.parent.txt_total.text))

    def on_completeproduct(self, w):
        print w.text
        if len(w.text) > 2:
            
            self.dropdown.clear_widgets()
            
            for item in devshub.root.inventario:
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
        inventoryitem.PUser = devshub.root.user
        
        inventoryitem.save()

        newitem = InventoryItem()
        w.text = "Save"
        
        table = self.parent.parent.parent.parent.lst_inventory
        
        table.add_widget(newitem, index=len(table.layout.children))

class Inventory(BoxLayout):
    lst_inventory = ObjectProperty()

class Main(BoxLayout):
    
    battleplan = ObjectProperty()
    
    def show_battleplan(self):
        
        if hasattr(self, "section"):
            self.remove_widget(self.section)
        else:
            self.remove_widget(self.battleplan)
            
        self.add_widget(self.battleplan)
        self.section = self.battleplan
        
    def show_ventas(self):
        print "Section ventas"
        
        if hasattr(self, "section"):
            self.remove_widget(self.section)
        else:
            self.remove_widget(self.battleplan)
            
        self.ventas = Pos()
        self.add_widget(self.ventas)
        self.section = self.ventas
    
    def show_inventario(self):        
        if hasattr(self, "section"):
            self.remove_widget(self.section)
        else:
            self.remove_widget(self.battleplan)
            
        self.inventario = Inventory()
        self.add_widget(self.inventario)
        self.section = self.inventario
        
    def show_servicios(self):        
        if hasattr(self, "section"):
            self.remove_widget(self.section)
        else:
            self.remove_widget(self.battleplan)
            
        self.inventario = Inventory()
        self.add_widget(self.inventario)
        self.section = self.inventario
        
    def show_rentas(self):        
        if hasattr(self, "section"):
            self.remove_widget(self.section)
        else:
            self.remove_widget(self.battleplan)
            
        self.inventario = Inventory()
        self.add_widget(self.inventario)
        self.section = self.inventario
        
    def show_organizacion(self):        
        if hasattr(self, "section"):
            self.remove_widget(self.section)
        else:
            self.remove_widget(self.battleplan)
            
        self.orgboat = Orgboat()
        self.add_widget(self.orgboat)
        self.section = self.orgboat
        
    def show_clientes(self):        
        if hasattr(self, "section"):
            self.remove_widget(self.section)
        else:
            self.remove_widget(self.battleplan)
            
        self.addclient = AddClient()
        self.add_widget(self.addclient)
        self.section = self.addclient

class DevsHub(FloatLayout):


    def saveClient(self, w):
        cliente = Clientes()
        cliente.Name = w.parent.txt_name.text
        cliente.Direccion = w.parent.txt_direccion.text
        cliente.Telefono = w.parent.txt_telefono.text
        cliente.IFE = w.parent.txt_ife.text
        cliente.Monedero = w.parent.txt_monedero.text
        cliente.save()

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
        
        self.inventario = Inventarios.Query.filter(PUser__in=[self.user])
        self.clientes = Clientes.Query.filter(PUser__in=[self.user])

if __name__ == "__main__":
    
    from kivy.app import App
    
    class DevsHubApp(App):
        def build(self):
            return DevsHub()

    #Asi para tener un objeto global y acceder al root widget
    app = DevsHubApp()
    app.run()
