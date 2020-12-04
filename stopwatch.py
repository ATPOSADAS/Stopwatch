import datetime
import time
import tkinter as tk
import tkinter.font as tkFont

#Based on code from user igniteflow - stopwatch.py

class Stopwatch(tk.Tk):
    def __init__(self, decimal_place):
        super().__init__()
        self.__swrun = True
        self.lap_count = 0
        self.decimal_place = decimal_place

        self.frm_sw = tk.Frame(master=self)
        self.frm_laptimes = tk.Frame(master=self)
        self.frm_btns = tk.Frame(master=self.frm_sw)

        #labels and lap times from the stopwatch
        fontStyle = tkFont.Font(family="Century Gothic", size=65)
        self.time_display = tk.StringVar(value="00:00."
                                               + (self.decimal_place-1)
                                               * "0")
        self.label = tk.Label(master=self.frm_sw, font=fontStyle,
                              textvariable=self.time_display)
        self.scrollbar = tk.Scrollbar(master=self.frm_laptimes)
        self.lap_list = tk.Listbox(master=self.frm_laptimes,
                                   yscrollcommand = self.scrollbar.set,
                                   width=35,
                                   font = tkFont.Font(family="Century Gothic"))
        self.scrollbar.config(command=self.lap_list.yview)

        #buttons
        self.btn_strp = tk.Button(master=self.frm_btns,
                                  text="Start",
                                  width=15,
                                  command=self.start)
        self.btn_rlap = tk.Button(master=self.frm_btns,
                                  text="Reset",
                                  width=15,
                                  state="disabled",
                                  command=None)

        #packing all the stuff
        self.frm_sw.pack()
        self.frm_laptimes.pack()
        self.frm_btns.grid(row=1, column=0)
        self.label.grid(row=0, column=0)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lap_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.btn_strp.pack(side=tk.LEFT, padx=15, pady=10)
        self.btn_rlap.pack(side=tk.LEFT, padx=15, pady=10)

    def start(self):
        "Initializes the necessary time variables and starts the stopwatch"
        self.__swrun = True
        self.start_time = datetime.datetime.now()
        self.split_time = self.start_time
        self.start_split = datetime.datetime.now() - self.start_time
        self.time_display.set(str(self.start_time - datetime.datetime.now()))

        self.btn_rlap["state"] = "normal"
        self.switch_btn_strp()
        self.switch_btn_rlap()
        self.elapsed()

    def resume(self):
        "Resumes the stopwatch, and resets start time variable"
        self.start_time = datetime.datetime.now() - self.elapsed_time
        self.__swrun = True

        self.switch_btn_strp()
        self.switch_btn_rlap()
        self.elapsed()

    def stop(self):
        "Stops the stopwatch"
        self.__swrun = False
        self.switch_btn_strp()
        self.switch_btn_rlap()

        #updates the time_display StringVar()
    def elapsed(self):
        """Emulates a stopwatch function by constantly updating StringVar()"""
        root.protocol('WM_DELETE_WINDOW', self.is_running)
        while self.__swrun:
            self.elapsed_time = datetime.datetime.now() - self.start_time
            self.time_display.set(self.format_datetime(self.elapsed_time))
            self.update()
            #error when application is closed or interrupted,
            #surround with try and catch

    #return a value at the exact moment a button is pressed
    def lap(self):
        """Records the split at current time from the last split and displays
        on the list"""
        self.split_time =  self.elapsed_time - self.start_split
        self.start_split = self.elapsed_time
        self.lap_count += 1
        self.lap_list.insert(0, str(self.lap_count) + "    "
                             + str(self.format_datetime(self.start_split))
                             + "          +"
                             + str(self.format_datetime(self.split_time)))

    def reset(self):
        "Resets all stopwatch variables and functions"
        self.btn_rlap["state"] = "disabled"
        self.switch_btn_strp(True)
        self.lap_count = 0
        self.lap_list.delete(0, tk.END)
        self.time_display.set("00:00." + (self.decimal_place-1)*"0")

    def switch_btn_strp(self, reset=False):
        "Switches the function and display of the start and stop buttons"
        if reset:
            self.btn_strp["command"] = self.start
        elif self.btn_strp["text"] == "Start":
            self.btn_strp["text"] = "Stop"
            self.btn_strp["command"] = self.stop
        elif self.btn_strp["text"] == "Stop":
            self.btn_strp["text"] = "Start"
            self.btn_strp["command"] = self.resume


    def switch_btn_rlap(self):
        "Switches the function and display of the reset and lap buttons"
        if self.btn_rlap["text"] == "Lap":
            self.btn_rlap["text"] = "Reset"
            self.btn_rlap["command"] = self.reset
        elif self.btn_rlap["text"] == "Reset":
            self.btn_rlap["text"] = "Lap"
            self.btn_rlap["command"] = self.lap

    def is_running(self):
        if not self.__swrun:
            root.destroy()

    def format_datetime(self, unf_time):
        """Returns a more readable and formatted version of datetime variable
        based on the chosen decimal place"""
        millisecond_index = str(unf_time).rfind(".") + self.decimal_place
        return str(unf_time)[:millisecond_index]


if __name__ == "__main__":
    root = Stopwatch(4)
    root.mainloop()
