
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty, NumericProperty

from kivy.animation import Animation
from kivy.clock import Clock

import os

from datepicker import DatePicker

from threading import Thread

try:
    from devslib.utils import MessageBoxTime
except:
    os.system("git clone https://github.com/oukiar/devslib")
    from devslib.utils import MessageBoxTime
    
from devslib.utils import alert
from devslib.utils import ImageButton
    
import time


from kivy.core.window import Window
Window.set_icon("pos.png")

class AsyncSave(Thread):
    def __init__(self, **kwargs):
        
        self.callback = kwargs.get("callback")
        self.objsave = kwargs.get("objsave")
        
        Thread.__init__(self)
        
        self.start()
        
    def run(self):
        self.objsave.save()
        Clock.schedule_once(self.callback, 0)

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
            
            for item in Clientes.Query.filter(words__all=w.text.upper().split() ):

                but = WhiteButton(text=item.Name, size_hint_y=None, height=40)
                but.bind(on_press=self.fillClient)
                but.Cliente = item
                self.dropdown.add_widget(but)
                found = True
                    
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
            
            #for item in app.root.inventarios:
            for item in app.root.inventarios:
                if w.text.upper() in item.Producto.upper():
                    but = WhiteButton(text=item.Producto, size_hint_y=None, height=40)
                    but.bind(on_press=self.fillProduct)
                    but.Item = item
                    self.dropdown.add_widget(but)
                    
            self.dropdown.open(w)
            
    def fillProduct(self, w):
        
        self.txt_producto.text = w.text
        self.txt_precio.text = w.Item.Precio
        if self.txt_cant.text != "":
            self.txt_total.text = str(float(self.txt_cant.text) * float(self.txt_precio.text))

        self.dropdown.dismiss()
        
class InventoryItem(BoxLayout):
    btn_save = ObjectProperty()
    btn_delete = ObjectProperty()

    def __init__(self, **kwargs):

        super(InventoryItem, self).__init__(**kwargs)

        self.btn_delete = ImageButton(source="delete.png", on_release=self.deleteInventory)
        self.btn_save = ImageButton(source="save.png", on_release=self.saveInventory)

    def editInventory(self):
        print "Edit inventory"
        self.txt_clave.disabled = False
        self.txt_producto.disabled = False
        self.txt_existencias.disabled = False
        self.txt_minimo.disabled = False
        self.txt_maximo.disabled = False
        self.txt_precio.disabled = False  
        
        self.txt_producto.focus = True

        self.lay_buttons.remove_widget(self.btn_edit)

        

        self.lay_buttons.add_widget(self.btn_delete)
        self.lay_buttons.add_widget(self.btn_save)

    def saveInventory(self, w):
        
        if not hasattr(self, "dataitem"):
            self.dataitem = Inventarios()
        
        self.dataitem.Clave = self.txt_clave.text
        self.dataitem.Producto = self.txt_producto.text
        self.dataitem.Existencias = self.txt_existencias.text
        self.dataitem.Minimo = self.txt_minimo.text
        self.dataitem.Maximo = self.txt_maximo.text
        self.dataitem.Precio = self.txt_precio.text
        self.dataitem.PUser = app.root.user
        
        #inventoryitem.save()
        AsyncSave(callback=self.item_saved, objsave=self.dataitem)
        
        self.lay_buttons.remove_widget(self.btn_delete)
        self.lay_buttons.remove_widget(self.btn_save)
        
        self.loading = RotatedImage(source="newloading.png")
        self.anim = Animation(angle=360, duration=5)
        self.anim.bind(on_complete=self.item_timeout)
        self.anim.start(self.loading)
        
        self.lay_buttons.add_widget(self.loading)
        
    def item_saved(self, dt):
        self.anim.cancel(self.loading)
        self.lay_buttons.remove_widget(self.loading)
        self.lay_buttons.add_widget(self.btn_edit)
        
        #disable all
        self.txt_clave.disabled = True
        self.txt_producto.disabled = True
        self.txt_existencias.disabled = True
        self.txt_minimo.disabled = True
        self.txt_maximo.disabled = True
        self.txt_precio.disabled = True 
    
    def item_timeout(self, anim, w):
        print "SAVE TIMEOUT"
        
    def deleteInventory(self, w):
        print "Deleting"
        self.dataitem.delete()
        
        app.root.inventario.lst_inventory.remove_widget(self)

class RotatedImage(Image):
    angle = NumericProperty()

class Inventory(BoxLayout):
    lst_inventory = ObjectProperty()

    def addInventoryItem(self, w):
        item = InventoryItem()
        
        item.txt_clave.disabled = False
        item.txt_producto.disabled = False
        item.txt_existencias.disabled = False
        item.txt_minimo.disabled = False
        item.txt_maximo.disabled = False
        item.txt_precio.disabled = False
        
        item.lay_buttons.remove_widget(item.btn_edit)
        item.lay_buttons.add_widget(item.btn_save)
        
        self.lst_inventory.add_widget(item, index=len(self.lst_inventory.layout.children) )
        
    def fillInventario(self):
        
        print "Llenado inventario"
        self.on_filtrar()

            
    def on_filtrar(self):
        print "Filtrando"
        
        self.lst_inventory.clear()
        
        if self.txt_filtrar.text != "":
        
            #for i in Inventarios.Query.filter(words__all=self.txt_filtrar.text.lower().split()).order_by("Producto"):
            for i in Inventarios.Query.filter(Producto__regex=self.txt_filtrar.text.upper(), PUser=app.root.user).order_by("Producto"):
                item = InventoryItem()
                item.dataitem = i
                item.txt_clave.text = str(i.Clave)
                item.txt_producto.text = str(i.Producto)
                item.txt_existencias.text = str(i.Existencias)
                item.txt_minimo.text = str(i.Minimo)
                item.txt_maximo.text = str(i.Maximo)
                item.txt_precio.text = str(i.Precio)
                            
                self.lst_inventory.add_widget(item)
                
                
        else:
            
            for i in app.root.inventarios:
                item = InventoryItem()
                item.dataitem = i
                item.txt_clave.text = str(i.Clave)
                item.txt_producto.text = str(i.Producto.encode('utf8'))
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
        
        self.inventarios = Inventarios.Query.filter(PUser__in=[self.user]).order_by("Producto")
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
