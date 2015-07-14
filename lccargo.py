
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock

from kivy.properties import ObjectProperty, StringProperty

from fbowidget import FboFloatLayout

#QR code library
import qrcode

#reportlab for generate the pdf file
from reportlab.pdfgen import canvas
point = 1
inch = 72

#parse stuff
from parse_rest.connection import register, ParseBatcher
from parse_rest.datatypes import Object
from parse_rest.user import User

#parse initialization
register("XEPryFHrd5Tztu45du5Z3kpqxDsweaP1Q0lt8JOb", "PE8FNw0hDdlvcHYYgxEnbUyxPkP9TAsPqKvdB4L0")
     
Receipts = Object.factory("Receipts")
Boxes = Object.factory("Boxes")

#Inventarios = Object.factory("Inventarios")
#Tareas = Object.factory("Tareas")
#Notas = Object.factory("Notas")


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
    
class NewReceipt(BoxLayout):
    tasks = ObjectProperty()
    tasktext = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(NewReceipt, self).__init__(**kwargs)
        

class Reports(BoxLayout):
    pass

class Commendations(BoxLayout):
    pass
	
class Stats(BoxLayout):
    labelBox = ObjectProperty()

class Orgboat(BoxLayout):

    menu = ObjectProperty()
    receipts = ObjectProperty()
    workSpace = ObjectProperty()

    def __init__(self, **kwargs):
        super(Orgboat, self).__init__(**kwargs)
        
        self.newreceipt = NewReceipt()
        self.reports = Reports()
        self.commendations = Commendations()
        self.stats = Stats()
        
        self.currentTab = self.receipts
        
    def changeTab(self, tabToShow):
        self.workSpace.remove_widget(self.currentTab)
        
        self.currentTab = tabToShow
        self.workSpace.add_widget(self.currentTab)
        
    def fillLabel(self):
        print "Getting information of the receipt: ", self.stats.receiptNum.text
        
        self.receipt = Receipts.Query.filter(ReceiptNum__in=[int(self.stats.receiptNum.text)])
        
        #the boxes
        self.boxes = Boxes.Query.filter(Receipt__in=[{"__type":"Pointer", "className":"Receipts", "objectId":self.receipt[0].objectId}])
        self.ibox = 0
        
        self.updateLabel()
        
    def updateLabel(self):
        #poner los valores en la etiqueta de impresion
        self.stats.companyName.text = self.receipt[0].Company.name
        self.stats.txt_receiptnum.text = str(self.receipt[0].ReceiptNum)
        self.stats.txt_destination.text = self.receipt[0].Destination
        self.stats.txt_shipper.text = self.receipt[0].Shipper.Name
        
        self.stats.txt_length.text = self.boxes[self.ibox].Length
        self.stats.txt_width.text = self.boxes[self.ibox].Width
        self.stats.txt_height.text = self.boxes[self.ibox].Height
        self.stats.txt_volume.text = self.receipt[0].Volume
        self.stats.txt_weightvol.text = self.receipt[0].WeightVol
        self.stats.txt_weight.text = self.boxes[self.ibox].Weight
        self.stats.txt_nbox.text = self.boxes[self.ibox].Num
        
        self.stats.txt_zone.text = self.receipt[0].Zone
        self.stats.txt_time.text = str(self.receipt[0].ReceiptDate)
        self.stats.txt_consignee.text = self.receipt[0].Consignee.Name
        self.stats.txt_madeby.text = self.receipt[0].Usr.Name
        
        
        img_qrcode = qrcode.make(self.boxes[self.ibox].objectId)
        img_qrcode.save(self.boxes[self.ibox].objectId + ".png")
        
        self.stats.img_qrcode.source = self.boxes[self.ibox].objectId + ".png"
        
        
        
    def printLabel(self):
        print "Printing"
        
        self.stats.remove_widget(self.stats.labelBox)
        
        self.laytemp = FboFloatLayout(size_hint=(None,None), size=(6*96,4*96))
        
        self.laytemp.add_widget(self.stats.labelBox)
        
        self.clear_widgets()
        
        self.add_widget(self.laytemp)
        
        Clock.schedule_once(self.do_save, 0)
        
    def do_save(self, dt):
        
        self.laytemp.texture.save(self.boxes[self.ibox].objectId + ".png")

        Clock.schedule_once(self.next_save, 0)

    def next_save(self, dt):
        if self.ibox < len(self.boxes)-1:
            self.ibox += 1
            self.updateLabel()
            Clock.schedule_once(self.do_save, 0)
            
        else:
            #create the PDF file
            c = canvas.Canvas("labels.pdf", pagesize=(6 * inch, 4 * inch))
            c.setStrokeColorRGB(0,0,0)
            c.setFillColorRGB(0,0,0)
            #c.setFont("Helvetica", 12 * point)
            
            for i in range(0, len(self.boxes) ):                            
                #image
                c.drawImage(self.boxes[i].objectId+".png", 0, 0, 6 * inch, 4 * inch)
                c.showPage()
            
            c.save()

if __name__ == "__main__":
    from kivy.app import App

    class LCCargoApp(App):
        def build(self):
            self.orgboat = Orgboat()
            return self.orgboat
        
    LCCargoApp().run()
