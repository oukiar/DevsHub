
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown

from kivy.properties import ObjectProperty, StringProperty

from datepicker import DatePicker

import os

from datetime import date, datetime, time, timedelta
import pytz

try:
    from devslib.utils import MessageBoxTime
    from devslib.scrollbox import ScrollBox
except:
    os.system("git clone https://github.com/oukiar/devslib")
    from devslib.utils import MessageBoxTime
    from devslib.scrollbox import ScrollBox



from kivy.core.window import Window
Window.set_icon("orgboat.png")

class SessionMenu(DropDown):
    pass

class SideMenu(BoxLayout):
    def openSessionMenu(self):
        self.menu = SessionMenu()
        self.menu.open(self.orgname)

class Profile(BoxLayout):
    def __init__(self, **kwargs):
        super(Profile, self).__init__(**kwargs)

        #self.jobactivities.updateList()

class TaskStatusMenu(BoxLayout):
    def on_changestatus(self, text):
        print text

        tarea = Tareas.Query.get(objectId=self.parent.taskID)
        tarea.Status = text
        tarea.save()

        app.root.battleplan.updateList()

        self.parent.remove_widget(self)

    def on_options(self):
        print "Opening options"

        tm = TaskMenu(taskItem=self.parent)
        tm.txt_tarea.text = self.parent.tasktext.text

        #obtener tarea
        tarea = Tareas.Query.get(objectId=self.parent.taskID)
        #inicializar valores en GUI
        tm.lst_status.text = tarea.Status

        tm.open()

    def on_close(self):
        print "Closing"
        self.parent.remove_widget(self)

class NewJobActivity(Popup):
    txt_title = ObjectProperty()
    txt_description = ObjectProperty()
    def addJobActivity(self):
        
        if self.btn_save.text == "Save":
            print "Updating job activity"
            
            jobactivity = JobActivities.Query.get(objectId=self.objectId)
            jobactivity.Title = self.txt_title.text
            jobactivity.Description = self.txt_description.text
            jobactivity.save()
            
            self.dismiss()
            
            #actualizar cache
            app.root.jobactivitiescache = JobActivities.Query.filter(PUser__in=[app.root.user]).order_by("-createdAt")
            
            #actualizar tabla
            app.root.profile.jobactivitiestable.updateList()
            
        else:
            print "Adding job activity"

            jobactivity = JobActivities()
            jobactivity.Title = self.txt_title.text
            jobactivity.Description = self.txt_description.text
            jobactivity.PUser = app.root.user
            jobactivity.save()

            self.dismiss()

            #add to the gui
            act = JobActivity()
            act.title.text = jobactivity.Title
            act.description.text = jobactivity.Description
            app.root.profile.jobactivitiestable.jobactivitieslist.add_widget(act)

class JobActivity(BoxLayout):
    def on_edit(self):
        editjob = NewJobActivity()
        editjob.txt_title.text = self.title.text
        editjob.txt_description.text = self.description.text
        editjob.btn_save.text = "Save"
        editjob.objectId = self.objectId
        editjob.open()

class JobActivitiesTable(BoxLayout):
    def updateList(self):
        
        self.jobactivitieslist.clear()   
        
        for jobact in app.root.jobactivitiescache:
            print jobact.Title

            act = JobActivity()
            act.objectId = jobact.objectId
            act.title.text = jobact.Title
            act.description.text = jobact.Description
            self.jobactivitieslist.add_widget(act)

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
        menu = TaskStatusMenu()
        self.add_widget(menu, len(self.children)-1)
        return

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
        tarea.PUser = app.root.user
        tarea.createdAtLocalTime = datetime.now(pytz.timezone('America/Mexico_City') )
        tarea.save()
        
        
        taskitem = BattlePlanItem()
        taskitem.tasktext.text = self.tasktext.text
        taskitem.taskID = tarea.objectId
        self.tasks.add_widget(taskitem, index=len(self.tasks.layout.children))

        #clean controls
        self.tasktext.text = ""
        #self.tasktext.focus = True
        
    def updateList(self):


        #filter
        if self.filter.text == 'Today':

            pub_date = datetime.now(pytz.timezone('America/Mexico_City') )
            min_pub_date_time = datetime.combine(pub_date, time.min)
            max_pub_date_time = datetime.combine(pub_date, time.max)

            print min_pub_date_time, max_pub_date_time

            tareas = Tareas.Query.filter(PUser__in=[app.root.user],
                                         createdAtLocalTime__gte=min_pub_date_time,
                                         createdAtLocalTime__lte=max_pub_date_time).order_by("-createdAt")
        elif self.filter.text == 'This week':

            dt = datetime.now(pytz.timezone('America/Mexico_City') )

            start = dt - timedelta(days = dt.weekday())
            end = start + timedelta(days = 6)

            tareas = Tareas.Query.filter(PUser__in=[app.root.user],
                                         createdAtLocalTime__gte=start,
                                         createdAtLocalTime__lte=end).order_by("-createdAt")
        elif self.filter.text == 'Yesterday':
            dt = datetime.now(pytz.timezone('America/Mexico_City') )
            dt = dt - timedelta(days = 1)
            dtmin = datetime.combine(dt, time.min)
            dtmax = datetime.combine(dt, time.max)
            print dtmin, dtmax
            tareas = Tareas.Query.filter(PUser__in=[app.root.user],
                                         createdAtLocalTime__gte=dtmin,
                                         createdAtLocalTime__lte=dtmax).order_by("-createdAt")
        elif self.filter.text == 'This month':
            tareas = Tareas.Query.filter(PUser__in=[app.root.user], createdAt__in=[datetime.datetime.today()]).order_by("-createdAt")
        elif self.filter.text == 'Last month':
            tareas = Tareas.Query.filter(PUser__in=[app.root.user], createdAt__in=[datetime.datetime.today()]).order_by("-createdAt")
        elif self.filter.text == 'Date interval':
            tareas = Tareas.Query.filter(PUser__in=[app.root.user], createdAt__in=[datetime.datetime.today()]).order_by("-createdAt")
        elif self.filter.text == 'Expireds':
            tareas = Tareas.Query.filter(PUser__in=[app.root.user], Status__in=['Expired']).order_by("-createdAt")
        elif self.filter.text == 'Pendings':
            tareas = Tareas.Query.filter(PUser__in=[app.root.user], Status__in=['Pending']).order_by("-createdAt")
        elif self.filter.text == 'In progress':
            tareas = Tareas.Query.filter(PUser__in=[app.root.user], Status__in=['In progress']).order_by("-createdAt")
        elif self.filter.text == 'Dones':
            tareas = Tareas.Query.filter(PUser__in=[app.root.user], Status__in=['Done']).order_by("-createdAt")

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

class Reports(BoxLayout):
    pass

class Commendations(BoxLayout):
    pass
	
class Stats(BoxLayout):
    pass

class Main(BoxLayout):
    pass
    

class Orgboat(BoxLayout):

    menu = ObjectProperty()
    profile = ObjectProperty()
    workSpace = ObjectProperty()

        
    def changeTab(self, tabToShow):
        if self.currentTab != None:
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
        self.main.txt_information.text = self.user.username
        self.add_widget(self.main)

        #create the sections of the user interface

        self.profile = Profile()
        self.battleplan = BattlePlan()
        self.reports = Reports()
        self.commendations = Commendations()
        self.stats = Stats()

        self.currentTab = None
        self.changeTab(self.profile)

        #self.main.workSpace.add_widget(self.profile)

        #add profile section as visible
        #self.main.workSpace.add_widget(self.profile)

        #cache de datos
        self.jobactivitiescache = JobActivities.Query.filter(PUser__in=[app.root.user]).order_by("-createdAt")

        #inicializar interfaz de usuario
        self.profile.jobactivitiestable.updateList()
        self.battleplan.updateList()

    def openNewJobActivity(self):
        NewJobActivity().open()

#parse stuff
try:
    Tareas = Object.factory("Tareas")
    JobActivities = Object.factory("JobActivities")
except:
    from parse_rest.connection import register, ParseBatcher
    from parse_rest.datatypes import Object
    from parse_rest.user import User

    #parse initialization
    register("hwKXR17rbtIP6ER9QL5AvQ5IM7ll17b1Iy3x4uTf", "1TifCFsTXIpUqlcZ0frTyCDHqW5HrCGtW10kqtpS")

    Tareas = Object.factory("Tareas")
    JobActivities = Object.factory("JobActivities")

    

if __name__ == "__main__":

    from kivy.app import App

    class OrgboatApp(App):
        def build(self):
            self.orgboat = Orgboat()
            return self.orgboat
            #return MyProfile()
        
    app = OrgboatApp()
    app.run()
