
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

from kivy.properties import ObjectProperty, StringProperty

from datepicker import DatePicker

#parse stuff
from parse_rest.connection import register, ParseBatcher
from parse_rest.datatypes import Object
from parse_rest.user import User

import time

#parse initialization
register("xIYoHZ0xgLwWIMWzQWPFtxrsZhzmpIQCFCAEJZch", "dqm0KGlhpaK9E0QoGi4dAMWmKuYokiutLegKeRPk")
     
Clientes = Object.factory("Clientes")
Inventarios = Object.factory("Inventarios")
Tareas = Object.factory("Tareas")

class AddClient(BoxLayout):
    pass

class Clientes(BoxLayout):
    pass

class Pos(BoxLayout):
    def hacerNota(self):
        print "Realizando nota"
        

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
        
        table = self.parent.parent.parent.parent.lst_note
        
        table.add_widget(newitem, index=len(table.layout.children))

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

class TaskMenu(Popup):
    
    taskItem = ObjectProperty()
    
    def selfDelete(self):
        print self.taskItem.taskID
                
        #delete from the database
        tarea = Tareas.Query.get(objectId=self.taskItem.taskID)
        tarea.delete()
        
        
        #update gui
        self.taskItem.parent.parent.parent.parent.updateList()
        
        #close this dialog
        self.dismiss()
        
    def selfSave(self):
        
        tarea = Tareas.Query.get(objectId=self.taskItem.taskID)
        tarea.Task = self.txt_tarea.text
        tarea.Status = self.lst_status.text
        tarea.save()
        
        self.taskItem.parent.parent.parent.parent.updateList()
        
        self.dismiss()

class BattlePlanItem(BoxLayout):
    taskID = StringProperty()
    
    def open_menu(self):
        tm = TaskMenu(taskItem=self)
        tm.txt_tarea.text = self.tasktext.text
        
        #obtener tarea
        tarea = Tareas.Query.get(objectId=self.taskID)
        #inicializar valores en GUI
        tm.lst_status.text = tarea.Status
        
        tm.open()
    
class BattlePlan(BoxLayout):
    tasks = ObjectProperty()
    tasktext = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(BattlePlan, self).__init__(**kwargs)
        #self.updateList()
    
    def addTask(self):
        tarea = Tareas()
        tarea.Task = self.tasktext.text
        tarea.Status = "Pending"
        tarea.PUser = devshub.root.user
        tarea.save()
        
        
        taskitem = BattlePlanItem()
        taskitem.tasktext.text = self.tasktext.text
        taskitem.taskID = tarea.objectId
        self.tasks.add_widget(taskitem, index=len(self.tasks.layout.children))

        #clean controls
        self.tasktext.text = ""
        #self.tasktext.focus = True
        
    def updateList(self):
        tareas = Tareas.Query.filter(PUser__in=[devshub.root.user]).order_by("-createdAt")

        self.tasks.clear()

        for tarea in tareas:
            taskitem = BattlePlanItem()
            taskitem.tasktext.text = tarea.Task
            taskitem.taskID = tarea.objectId
            
            if tarea.Status == "Pending":
                taskitem.img_menu.source = "menu_pending.png"
            elif tarea.Status == "In progress":
                taskitem.img_menu.source = "menu_inprogress.png"
            elif tarea.Status == "Done":
                taskitem.img_menu.source = "menu_done.png"
            elif tarea.Status == "Expired":
                taskitem.img_menu.source = "menu_expired.png"
            
            self.tasks.add_widget(taskitem)

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
            
        self.inventario = Inventory()
        self.add_widget(self.inventario)
        self.section = self.inventario
        
    def show_clientes(self):        
        if hasattr(self, "section"):
            self.remove_widget(self.section)
        else:
            self.remove_widget(self.battleplan)
            
        self.clientes = Clientes()
        self.add_widget(self.clientes)
        self.section = self.clientes

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
        self.main.battleplan.updateList()
        self.add_widget(self.main)
        
        self.inventario = Inventarios.Query.filter(PUser__in=[self.user])

if __name__ == "__main__":
    
    from kivy.app import App
    
    class DevsHubApp(App):
        def build(self):
            return DevsHub()

    #Asi para tener un objeto global y acceder al root widget
    devshub = DevsHubApp()
    devshub.run()
