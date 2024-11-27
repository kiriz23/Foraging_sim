#Kyrylo Krocha

#Modules
import matplotlib
matplotlib.use('TkAgg')
import pylab
import time
from tkinter import *
from tkinter.ttk import Notebook


class UI:

    def __init__(self, title = "Drawer", interval=0, step_size=1,time_limit=0):
        self.title_text = title
        self.time_interval = interval
        self.step_size = step_size
        self.time_limit = time_limit
        self.var_entries = {}
        self.status_str = ""
        self.running = False
        self.model_figure = None
        self.current_step = 0

        self.start_time = 0
        self.total_pause_time = 0
        self.pause_time = 0

        #root window
        self.root_window = Tk()
        self.status_text = StringVar(self.root_window, value=self.status_str)
        self.set_status_str("Моделювання ще не почалось")

        self.root_window.wm_title(self.title_text)
        self.root_window.protocol('WM_DELETE_WINDOW', self.quitUI)
        self.root_window.geometry('400x260')
        self.root_window.columnconfigure(0, weight=1)
        self.root_window.rowconfigure(0, weight=1)
        self.notebook = Notebook(self.root_window)
        self.notebook.pack(side=TOP, padx=2, pady=2)

        self.frame_run = Frame(self.root_window)
        self.frame_settings = Frame(self.root_window)

        self.notebook.add(self.frame_run, text="Початок")


        self.notebook.pack(expand=NO, fill=BOTH, padx=5, pady=5, side=TOP)

        self.status = Label(self.root_window, width=40, height=3, bd=1, textvariable=self.status_text)
        self.status.pack(side=TOP, fill=X, padx=5, pady=5, expand=NO)

        self.run_pause_string = StringVar(self.root_window)
        self.run_pause_string.set("Почати")
        self.button_run = Button(self.frame_run, width=30, height=2, textvariable=self.run_pause_string,
                                command=self.run_event)
        self.button_run.pack(side=TOP, padx=5, pady=5)

        self.button_step = Button(self.frame_run, width=30, height=2, text='Один крок', command=self.step_once)
        self.button_step.pack(side=TOP, padx=5, pady=5)

        self.button_reset = Button(self.frame_run, width=30, height=2, text='Почати знову', command=self.reset_model)
        self.button_reset.pack(side=TOP, padx=5, pady=5)


        #settings






    def run_event(self):
        if not(self.start_time):
            self.start_time = time.time()
        self.running = not self.running
        if self.running:
            if (self.pause_time):
                self.total_pause_time += abs(self.pause_time-time.time())
                self.pause_time = 0
            self.root_window.after(self.time_interval, self.step_model)
            self.run_pause_string.set("Пауза")
            self.button_step.configure(state=DISABLED)
            self.button_reset.configure(state=DISABLED)

        else:
            if not (self.pause_time):
                self.pause_time = time.time()
            self.run_pause_string.set("Продовжити")
            self.button_step.configure(state=NORMAL)
            self.button_reset.configure(state=NORMAL)


    def step_model(self):
        if (abs(self.start_time - time.time() + self.total_pause_time) >= self.time_limit):
            self.running = 0
            self.quitUI()
        if self.running:
            self.model_step_func()
            self.current_step += 1
            self.set_status_str("Крок " + str(self.current_step))
            self.status.configure(foreground='black')
            if (self.current_step) % self.step_size == 0:
                self.draw_model()
            self.root_window.after(int(self.time_interval * 1.0 / self.step_size), self.step_model)


    def step_once(self):
        self.running = False
        self.run_pause_string.set("Продовжити")
        self.model_step_func()
        self.current_step += 1
        self.set_status_str("Крок " + str(self.current_step))
        self.draw_model()


    def reset_model(self):
        self.running = False
        self.run_pause_string.set("Почати")
        self.model_init_func()
        self.current_step = 0
        self.set_status_str("Відбувся перезапуск")
        self.draw_model()


    def draw_model(self):
        pylab.ion()
        if self.model_figure == None or self.model_figure.canvas.manager.window == None:
            self.model_figure = pylab.figure()
        self.model_draw_func()
        self.model_figure.canvas.manager.window.update()
        pylab.show()


    def start(self, func=[]):
        if len(func) == 3:
            self.model_init_func = func[0]
            self.model_draw_func = func[1]
            self.model_step_func = func[2]
            self.model_init_func()
            self.draw_model()
        self.root_window.mainloop()


    def change_step_size(self, val):
        self.stepSize = val


    def set_status_str(self, new_status):
        self.status_str = new_status
        self.status_text.set(self.status_str)


    def quitUI(self):
        pylab.close('all')
        self.root_window.quit()
        self.root_window.destroy()