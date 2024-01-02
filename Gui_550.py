import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import * 
'''Frame, Tk, Scrollbar, HORIZONTAL, VERTICAL, BOTH, BOTTOM, RIGHT, LEFT, Y, N, S, E, W'''
import customtkinter
import os
import csv
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import time
from functools import partial
from dateutil.parser import parse
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pyautogui



customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
plt.rcParams['text.color'] = 'white'
plt.rcParams['grid.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['patch.facecolor'] = 'black'
plt.rcParams['axes.facecolor'] = 'black'
plt.rcParams['axes.xmargin'] = 0
plt.rcParams['axes.ymargin'] = 1
#matplotlib.use('TkAgg')



#create class to load data from CSV files into pandas data frames
class Data_Loader():
	def __init__(self):
		self.id = id
		self.dataframe = None
		self.days = []
		self.local = None
		

	def loader(self, rel_path):
		dirname = os.path.dirname(__file__)
		abs_path = os.path.join(dirname, rel_path)
		with open(abs_path, 'r') as f:
			Sub_df = pd.read_csv(f)
			return(Sub_df)
		
	def mini_loader(self, rel_path):
		dirname = os.path.dirname(__file__)
		abs_path = os.path.join(dirname, rel_path)
		fields = ['Datetime (UTC)']
		if self.local is None:
			with open(abs_path, 'r') as f:
				new = pd.read_csv(f, nrows=1, usecols=['Timezone (minutes)'])
				self.local = int(new['Timezone (minutes)'].iloc[0])
		with open(abs_path, 'r') as f:
			Sub_df = pd.read_csv(f , skipinitialspace=True, usecols=fields)
			#print(Sub_df)
			return(Sub_df)
		

	def dataframe_creation(self, start, finish):
		#loop to run through each file marked by the date
		Subject_df = pd.DataFrame()
		pd.set_option("display.max_columns", None)
		pd.set_option('display.width', None)
		pd.set_option('display.max_colwidth', None)
		pd.set_option("display.max_rows", None)
		for i in range (20200118, 20200122):
			try:
				Sub_df=self.loader('Dataset\\'+str(i)+'\\'+str(self.id)+'\\summary.csv')
				Subject_df = pd.concat([Subject_df, Sub_df])
			except FileNotFoundError:
				print("Subject " + str(self.id) + " did not have files in folder " + str(i))

		mask = (Subject_df['Datetime (UTC)'] > start) & (Subject_df['Datetime (UTC)'] <= finish)
		df2 = Subject_df.loc[mask]
		df2 = df2.drop_duplicates(subset=['Datetime (UTC)'], keep='first',inplace=False)

		return(df2)
	
	
	def mini_dataframe_creation(self):
		Subject_df = pd.DataFrame()
		for i in range (20200118, 20200122):
			try:
				Sub_df=self.mini_loader('Dataset\\'+str(i)+'\\'+str(self.id)+'\\summary.csv')
				Subject_df = pd.concat([Subject_df, Sub_df])
			except FileNotFoundError:
				print("Subject " + str(self.id) + " did not have files in folder " + str(i))
		return(Subject_df)


class data_visualizer(Figure):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.patch.set_facecolor('black')

	def graph_type(self, tuple, fig):
		if tuple[1]==3:
			fig.suptitle('Acc magnitude avg')
			return('Acc magnitude avg')
		elif tuple[1]==4:
			fig.suptitle('Eda avg')
			return('Eda avg')
		elif tuple[1]==5:
			fig.suptitle('Temp avg')
			return('Temp avg')
		elif tuple[1]==6:
			fig.suptitle('Movement intensity')
			return('Movement intensity')
		elif tuple[1]==7:
			fig.suptitle('Steps count')
			return('Steps count')
		elif tuple[1]==8:
			fig.suptitle('Rest')
			return('Rest')
		elif tuple[1]==9:
			fig.suptitle('On Wrist')
			return('On Wrist')

#creation of class instances and data frames for each participant of the study
Sub_list = []
Subject_1 = Data_Loader()
Subject_2 = Data_Loader()
Subject_3 = Data_Loader()
Subject_1.id = '310'
Subject_2.id = '311'
Subject_3.id = '312'
Sub_list.append(Subject_1)
Sub_list.append(Subject_2)
Sub_list.append(Subject_3)

vals=[]
for i in range(len(Sub_list)):
	vals.append(Sub_list[i].id)


class App(customtkinter.CTk):
	def __init__(self):
		super().__init__()

		#configure main window
		self.title("VisuaLive")
		self.geometry(f"{1300}x{750}")
		#self.rowconfigure(0, weight=1)
		#self.columnconfigure(0, weight=1)


		#configure grid layout
		self.grid_columnconfigure((0), weight=1)
		self.grid_columnconfigure((1), weight=15)
		self.grid_columnconfigure((3), weight=1)
		#self.grid_columnconfigure(4, weight=2)
		self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)

		#create sidebar frame with widgets
		self.sidebar_frame = customtkinter.CTkFrame(self, width=75, corner_radius=10)
		self.sidebar_frame_2 = customtkinter.CTkScrollableFrame(self, width=100, corner_radius=10)
		self.sidebar_frame_3 = customtkinter.CTkFrame(self, width=100, corner_radius=10)
		self.sidebar_frame.grid(row=0, column=0, rowspan=7, padx=10, pady=10, sticky="new")
		#self.sidebar_frame_2.grid(row=0, column=1, rowspan=7, padx=10, pady=10, sticky="new")

		#Main label creation
		self.title_label = customtkinter.CTkLabel(self.sidebar_frame, text="VisuaLive", font=customtkinter.CTkFont(family="Times", size=40, weight="bold", slant="italic"))
		self.title_label.grid(row=0, column=0, padx=(10, 10), pady=10)

		self.subtitle_label = customtkinter.CTkLabel(self.sidebar_frame, text="Physical Tracker", font=customtkinter.CTkFont(family="Times", size=24, weight="bold", slant="italic"))
		self.subtitle_label.grid(row=0, column=1, pady=10, sticky="sew")
		
		self.index_label = customtkinter.CTkLabel(self.sidebar_frame, text="Index", font=customtkinter.CTkFont(size=16)) 
		self.index_label.grid(row=2, column=0, padx=20, sticky="nse")

		#Combobox creation

		#Summary box
		self.combobox1 = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Summary"], command=self.optionmenu_index)
		self.combobox1.grid(row=2, column=1, columnspan=2, pady=10, sticky="nsew")
		self.combobox1.set("Summary")

		#Subject box
		self.subjects_label = customtkinter.CTkLabel(self.sidebar_frame, text="Subject", font=customtkinter.CTkFont(size=16)) 
		self.subjects_label.grid(row=4, column=0, padx=20, pady=10, sticky="nse")
		self.combobox2 = customtkinter.CTkComboBox(self.sidebar_frame, values=["Please select a timezone"], command=self.select_subject)
		self.combobox2.grid(row=4, column=1, columnspan=2, pady=10, sticky="nsew")
		self.combobox2.set("Subjects")
		#self.combobox2.configure(values = vals) #vals is created at line 87
		

		self.date_time_range_label = customtkinter.CTkLabel(self.sidebar_frame, text="Date/Time Range", font=customtkinter.CTkFont(size=16)) 
		self.date_time_range_label.grid(row=11, column=0, padx=20, pady=10, sticky="nse")
		
		self.time_var = customtkinter.StringVar()
		self.combobox3 = customtkinter.CTkComboBox(self.sidebar_frame, values=["Please select a starting and ending day"], command=self.optionmenu_date_time_start)
		self.combobox3.grid(row=11,  columnspan=1, column=2, ipadx=.5, pady=10, sticky="nsew")
		self.combobox3.set("Time Start")

		self.combobox5 = customtkinter.CTkOptionMenu(self.sidebar_frame, values=['Please select a subject'])
		#self.combobox5.configure(command=partial(self.select_day, self.combobox5, self.combobox6, self.optionmenu_subject))
		self.combobox5.grid(row=11, columnspan=1, column=1, ipadx=.5, pady=10, sticky="nsew")
		self.combobox5.set("Day")
		
		self.combobox4 = customtkinter.CTkComboBox(self.sidebar_frame, values=["Please select a starting and ending day"], command=self.optionmenu_date_time_end)
		self.combobox4.grid(row=12, columnspan=1, column=2, ipadx=.5, pady=10, sticky="nsew")
		self.combobox4.set("Time Finish")

		self.combobox6 = customtkinter.CTkOptionMenu(self.sidebar_frame, values=['Please select a subject'])
		self.combobox6.configure(command=partial(self.select_day, self.combobox5,  self.combobox6, self.optionmenu_subject))
		self.combobox6.grid(row=12, columnspan=1, column=1, ipadx=.5, pady=10, sticky="nsew")
		self.combobox6.set("Day")

		self.time_zone_label = customtkinter.CTkLabel(self.sidebar_frame, text="Time Zone", font=customtkinter.CTkFont(size=16)) 
		self.time_zone_label.grid(row=3, column=0, padx=20, pady=10, sticky="nse")

		#Checkbox creation
		self.prompt_label = customtkinter.CTkLabel(self.sidebar_frame, text="Columns to Import", font=customtkinter.CTkFont(size=16))
		self.prompt_label.grid(row=5, column=0, padx=20, pady=10)

		self.check_var_1 = customtkinter.IntVar()
		self.check_var_2 = customtkinter.IntVar()
		self.check_var_3 = customtkinter.IntVar()
		self.check_var_4 = customtkinter.IntVar()
		self.check_var_5 = customtkinter.IntVar()
		self.check_var_6 = customtkinter.IntVar()
		self.check_var_7 = customtkinter.IntVar()
		self.check_var_8 = customtkinter.IntVar()
		self.check_var_9 = customtkinter.IntVar()
		
		self.checkbox1 = customtkinter.CTkCheckBox(self.sidebar_frame, text="Acc Mag Avg", variable=self.check_var_1, offvalue=0, onvalue=1, command=self.optionmenu_device)
		self.checkbox2 = customtkinter.CTkCheckBox(self.sidebar_frame, text="EDA Avg", variable=self.check_var_2, offvalue=0, onvalue=1, command=self.optionmenu_device)
		self.checkbox3 = customtkinter.CTkCheckBox(self.sidebar_frame, text="Temp Avg", variable=self.check_var_3, offvalue=0, onvalue=1, command=self.optionmenu_device)
		self.checkbox4 = customtkinter.CTkCheckBox(self.sidebar_frame, text="Movement Intensity", variable=self.check_var_4, offvalue=0, onvalue=1, command=self.optionmenu_device)
		self.checkbox5 = customtkinter.CTkCheckBox(self.sidebar_frame, text="Steps Count", variable=self.check_var_5, offvalue=0, onvalue=1, command=self.optionmenu_device)
		self.checkbox6 = customtkinter.CTkCheckBox(self.sidebar_frame, text="At Rest", variable=self.check_var_6, offvalue=0, onvalue=1, command=self.optionmenu_device)
		self.checkbox7 = customtkinter.CTkCheckBox(self.sidebar_frame, text="On Wrist", variable=self.check_var_7, offvalue=0, onvalue=1, command=self.optionmenu_device)

		self.checkbox8 = customtkinter.CTkCheckBox(self.sidebar_frame, text="UTC", variable=self.check_var_8, offvalue=0, onvalue=1, command=partial(self.optionmenu_timezone, self.check_var_8, self.check_var_9))
		self.checkbox9 = customtkinter.CTkCheckBox(self.sidebar_frame, text="Local", variable=self.check_var_9, offvalue=0, onvalue=1, command=partial(self.optionmenu_timezone, self.check_var_9, self.check_var_8))

		self.checkbox1.grid(row=5, column=1, columnspan=2, pady=10, sticky="nsew")
		self.checkbox2.grid(row=5, column=2, columnspan=2, pady=10, sticky="nsew")
		self.checkbox3.grid(row=6, column=1, columnspan=2, pady=10, sticky="nsew")
		self.checkbox4.grid(row=6, column=2, columnspan=2, pady=10, sticky="nsew")
		self.checkbox5.grid(row=7, column=1, columnspan=2, pady=10, sticky="nsew")
		self.checkbox6.grid(row=7, column=2, columnspan=2, pady=10, sticky="nsew")
		self.checkbox7.grid(row=8, column=1, columnspan=2, pady=10, sticky="nsew")

		self.checkbox8.grid(row=3, column=1, columnspan=2, pady=10, sticky="nsew")
		self.checkbox9.grid(row=3, column=2, columnspan=2, pady=10, sticky="nsew")
  
		self.right_menu = Menu(self, tearoff=False)
		self.right_menu.add_command(label="Line Plot", command=self.line)
		self.right_menu.add_command(label="Scatter Plot", command=self.scatter)
		self.right_menu.add_command(label="Bar Plot", command=self.bar)
		self.right_menu.add_command(label="Exit", command=self.quit())
  
		#self.figure_canvas_1bind("<Button-3>", self.right_popup)

		self.import_button = customtkinter.CTkButton(self.sidebar_frame, text="Import Data", command=partial(self.sidebar_import_button, self.optionmenu_date_time_start, self.optionmenu_date_time_end, self.optionmenu_subject, self.optionmenu_device))
		self.import_button.grid(row=13, column=1, columnspan=2, padx=20, pady=10, sticky="nsew")
		
		self.clear_button = customtkinter.CTkButton(self.sidebar_frame, text="Clear Entries", command=partial(self.sidebar_clear_button, self.optionmenu_date_time_start, self.optionmenu_date_time_end, self.optionmenu_subject, self.optionmenu_device))
		self.clear_button.grid(row=14, column=1, columnspan=2, padx=20, pady=10, sticky="nsew")

		self.graph_1=[0]
		self.graph_2=[0]
		self.graph_3=[0]
		self.graph_4=[0]
		self.graph_5=[0]
		self.graph_6=[0]
		self.graph_7=[0]
   	

	def line(self):
		f=self.right_menu.f
		print(f)
		if f==1:
			self.graph_1.append(0)
		if f==2:
			self.graph_2.append(0)
		if f==3:
			self.graph_3.append(0)
		if f==4:
			self.graph_4.append(0)
		if f==5:
			self.graph_5.append(0)
		if f==6:
			self.graph_6.append(0)
		if f==7:
			self.graph_7.append(0)
		
		
	def scatter(self):
		f=self.right_menu.f
		print(f)
		if f==1:
			self.graph_1.append(1)
		if f==2:
			self.graph_2.append(1)
		if f==3:
			self.graph_3.append(1)
		if f==4:
			self.graph_4.append(1)
		if f==5:
			self.graph_5.append(1)
		if f==6:
			self.graph_6.append(1)
		if f==7:
			self.graph_7.append(1)

	def bar(self):
		f=self.right_menu.f
		print(f)
		if f==1:
			self.graph_1.append(2)
		if f==2:
			self.graph_2.append(2)
		if f==3:
			self.graph_3.append(2)
		if f==4:
			self.graph_4.append(2)
		if f==5:
			self.graph_5.append(2)
		if f==6:
			self.graph_6.append(2)
		if f==7:
			self.graph_7.append(2)

	def time_of_day(self, dates, combobox1):
		time_of_day=[]
		for date in dates:
			if date.split('T')[0]==combobox1.get():
				time_of_day.append(str(date.split('T')[-1])[:-1])
		return(time_of_day)
	
	def time_import(self, subject):
		subject.dataframe=subject.mini_dataframe_creation()
		for i in subject.dataframe['Datetime (UTC)']:
			s=i
			f = '%Y-%m-%dT%H:%M:%SZ'
			
			out = datetime.strptime(s, f)
			if self.checkbox9.get()==1:
				out-timedelta(minutes=subject.local)
			out = out.strftime('%Y-%m-%d')
			if (out) not in subject.days:
				subject.days.append(out)
		return(subject.days)
		
	def select_subject(self, subject):
		days = self.time_import(self.optionmenu_subject(self.combobox2.get()))
		new_days=[]
		for i in days:
			string=str(i)
			string=string.replace(", ", "-")
			new_days.append(string)

		self.combobox5.configure(values=new_days)
		self.combobox6.configure(values=new_days)

	def select_day(self, combobox1, combobox2, subject, event):
		Subject=subject(self)
		dates=[]
		
		for date in Subject.dataframe['Datetime (UTC)']:
			if self.check_var_9.get()==1:
				date=datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
				date=date+timedelta(minutes=Subject.local)
				date=datetime.strftime(date, '%Y-%m-%dT%H:%M:%SZ')
				if date.split('T')[0]<=combobox2.get() and date.split('T')[0]>=combobox1.get():
					dates.append(date)
			elif self.check_var_8.get()==1:
				if date.split('T')[0]<=combobox2.get() and date.split('T')[0]>=combobox1.get():
					dates.append(date)

		time_of_day_start=self.time_of_day(dates, combobox1)
		time_of_day_end=self.time_of_day(dates, combobox2)
		

		Subject.dataframe = Subject.dataframe_creation(dates[0], dates[-1])		

		time_of_day_start_new=time_of_day_start[::2]
		time_of_day_end_new=time_of_day_end[::2]

		self.combobox3.configure(values=time_of_day_start_new)
		self.combobox4.configure(values=time_of_day_end_new)
		
		
	def optionmenu_index(self, summary):
		print("optionmenu1 dropdown clicked:")

	def optionmenu_subject(self, subject):
		subject = self.combobox2.get()
		for count, i in enumerate(Sub_list):
			if subject == Sub_list[count].id:
				return(Sub_list[count])
			else:
				pass
			
	def optionmenu_device(self):
		checked_list=[0]
		if self.check_var_1.get()==1:
			checked_list.append(3)
		if self.check_var_2.get()==1:
			checked_list.append(4)
		if self.check_var_3.get()==1:
			checked_list.append(5)
		if self.check_var_4.get()==1:
			checked_list.append(6)
		if self.check_var_5.get()==1:
			checked_list.append(7)
		if self.check_var_6.get()==1:
			checked_list.append(8)
		if self.check_var_7.get()==1:
			checked_list.append(9)
		print(checked_list)
		return(checked_list)
	
	def optionmenu_timezone(self, var1, var2):
		self.combobox2.configure(values = vals)
		if var1.get()==1:
			var2.set(0)
		

	def optionmenu_date_time_start(self, date):
		time_var_1=(self.combobox3.get())
		time_var_2=(self.combobox5.get())
		start=(time_var_2+'T'+time_var_1+'Z')
		return(start)

	def optionmenu_date_time_end(self, date):
		time_var_1=(self.combobox4.get())
		time_var_2=(self.combobox6.get())
		end=(time_var_2+'T'+time_var_1+'Z')
		return(end)
	
	def sidebar_import_button(self, start, end, subject, list):
		start_date = start(self)
		end_date = end(self)
		Subject = subject(self)
		Check_list = list()
		mask = (Subject.dataframe['Datetime (UTC)'] > start_date) & (Subject.dataframe['Datetime (UTC)'] <= end_date)
		df2 = Subject.dataframe.loc[mask]
		df2=df2.iloc[:,Check_list]

		self.figure_creation(df2, Check_list, subject)
		
	#def create_rectangle(self):
		#self.current_shape = "rectangle"
  		
	def start_draw(self, event, dataframe, ax):
		self.start_x = event.x
		self.start_y = event.y
		data_x=ax.transData.inverted().transform((event.x, 0))[0]
		'''if self.current_shape == "rectangle":
			self.current_shape_item = self.create_rectangle(
                self.start_x, self.start_y, self.start_x, self.start_y, outline="black"
            )
		print(self.start_x, self.start_y, self.start_x, self.start_y)'''
		#return (self.start_x, self.start_y)
		closest_date = min(dataframe.index, key=lambda x: abs((x - data_x)))
		self.value_at_click_1 = dataframe.loc(axis=0)[closest_date, 'Datetime (UTC)']
		#print(self.value_at_click_1)
		
		
 
	def stop_draw(self, event, dataframe, ax):
		self.end_x = event.x
		self.end_y = event.y
		data_x=ax.transData.inverted().transform((event.x, 0))[0]
		dist_start=(self.start_x)
		#dist_end=(self.end_x-dist_start)
		if self.current_shape == "rectangle":
			self.current_shape_item = self.create_rectangle(
                self.start_x, self.end_x, outline="black"
            )
		#print(data_x)
		closest_date = min(dataframe.index, key=lambda x: abs((x - data_x)))
		#print(closest_date)
		self.value_at_click_2 = dataframe.loc(axis=0)[closest_date, 'Datetime (UTC)']
		print(self.value_at_click_2)

		self.new_window=Toplevel(self)
		self.new_window.geometry("800x800")

		self.figure_side = data_visualizer(figsize=(8, 8))
		#self.sidebar_frame_3.grid(row=0, column=3, rowspan=7, padx=10, pady=10, sticky="new")
		self.figure_side_canvas = FigureCanvasTkAgg(self.figure_side, self.new_window)
		self.figure_side_canvas.get_tk_widget().grid(row=1, column=3, padx=5, pady=5, sticky="nsew")
		self.axes_2 = self.figure_side.add_subplot()
		mask=(dataframe['Datetime (UTC)'] > self.value_at_click_1) & (dataframe['Datetime (UTC)']  <= self.value_at_click_2)
		#print(mask)
		df2 = dataframe.loc[mask]
		print(df2)
		#df2=df2.iloc[:,tuple]
		
		
		
		self.axes_2.plot(df2.iloc[:,0], df2.iloc[:,1])
		
		
            
	def right_popup(self, event, f):
		if event.dblclick:
			coord=pyautogui.position()
			x=coord.x
			y=coord.y
			#print(coord)
			#print(f)
			self.right_menu.tk_popup(x,y)
		if f==1:
			self.right_menu.f=1
		if f==2:
			self.right_menu.f=2
		if f==3:
			self.right_menu.f=3
		if f==4:
			self.right_menu.f=4
		if f==5:
			self.right_menu.f=5
		if f==6:
			self.right_menu.f=6
		if f==7:
			self.right_menu.f=7
	
    
    #def change_plot(self, x, dataframe):
            
      
	def figure_creation(self, dataframe, list, subject):
		self.figure_1 = data_visualizer(figsize=(8, 8))
		self.figure_2 = data_visualizer(figsize=(8, 8))
		self.figure_3 = data_visualizer(figsize=(8, 8))
		self.figure_4 = data_visualizer(figsize=(8, 8))
		self.figure_5 = data_visualizer(figsize=(8, 8))
		self.figure_6 = data_visualizer(figsize=(8, 8))
		self.figure_7 = data_visualizer(figsize=(8, 8))
  
		def graph(g, x, dataframe):
			if g==0:
				self.axes.plot(x, dataframe)
			if g==1:
				self.axes.scatter(x, dataframe)
			elif g==2:
				self.axes.bar(x, dataframe)
			print()

		#place figure object
		tuple_1=(list[0],list[1])

		self.sidebar_frame_2.grid(row=0, column=1, rowspan=7, padx=10, pady=10, sticky="nsew")

		
		self.figure_canvas_1 = FigureCanvasTkAgg(self.figure_1, self.sidebar_frame_2)
		#self.graph = [0]
		self.figure_canvas_1.get_tk_widget().grid(row=1, column=3, padx=5, pady=5, sticky="nsw")
		self.axes = self.figure_1.add_subplot()
  
  
  
		x = dataframe['Datetime (UTC)']
		print(x)
		graph(self.graph_1[-1], x, dataframe[data_visualizer.graph_type(self, tuple_1, self.figure_1)])
		
   
		print(self.axes.get_xticks()[1])
		self.axes.set_xticks(self.axes.get_xticks()[::(round(len(x)/3))])

		self.toolbar = NavigationToolbar2Tk(self.figure_canvas_1, self, pack_toolbar=False)
		self.toolbar.update()

		self.current_shape = None
		self.start_x = None
		self.start_y = None
		self.current_shape_item = None
  
		self.figure_canvas_1.mpl_connect("button_press_event", lambda event: self.start_draw(event, dataframe, self.axes))
		self.figure_canvas_1.mpl_connect("button_release_event", lambda event: self.stop_draw(event, dataframe, self.axes))
  
		self.figure_canvas_1.mpl_connect("button_press_event", lambda event: self.right_popup(event, 1))
  
		
		if len(list)>2:
			tuple_2=(list[0],list[2])
			self.figure_canvas_2 = FigureCanvasTkAgg(self.figure_2, self.sidebar_frame_2)
			#self.figure_canvas_2.graph = [0]
			self.figure_canvas_2.get_tk_widget().grid(row=2, column=3, padx=5, pady=5, sticky="nsw")
			self.axes = self.figure_2.add_subplot()
			#self.axes.plot(x, dataframe[data_visualizer.graph_type(self, tuple_2, self.figure_2)])
			graph(self.graph_2[-1], x, dataframe[data_visualizer.graph_type(self, tuple_2, self.figure_2)])
			self.figure_canvas_2.mpl_connect("button_press_event", lambda event: self.right_popup(event, 2))
			self.axes.set_xticks(self.axes.get_xticks()[::(round(len(x)/3))])
			#self.figure_canvas_2.mpl_connect("button_press_event", lambda event: self.start_draw(event, dataframe, self.axes))
			#self.figure_canvas_2.mpl_connect("button_release_event", lambda event: self.stop_draw(event, dataframe, self.axes))

		if len(list)>3:
			tuple_3=(list[0],list[3])
			self.figure_canvas_3 = FigureCanvasTkAgg(self.figure_3, self.sidebar_frame_2)
			#self.figure_canvas_3.graph = [0]
			self.figure_canvas_3.get_tk_widget().grid(row=3, column=3, padx=5, pady=5, sticky="nsw")
			self.axes = self.figure_3.add_subplot()
			#self.axes.plot(x, dataframe[data_visualizer.graph_type(self, tuple_3, self.figure_3)])
			graph(self.graph_3[-1], x, dataframe[data_visualizer.graph_type(self, tuple_3, self.figure_3)])
			self.figure_canvas_3.mpl_connect("button_press_event", lambda event: self.right_popup(event, 3))
			self.axes.set_xticks(self.axes.get_xticks()[::(round(len(x)/3))])

		if len(list)>4:
			tuple_4=(list[0],list[4])
			self.figure_canvas_4 = FigureCanvasTkAgg(self.figure_4, self.sidebar_frame_2)
			#self.figure_canvas_4.graph = [0]
			self.figure_canvas_4.get_tk_widget().grid(row=4, column=3, padx=5, pady=5, sticky="nsw")
			self.axes = self.figure_4.add_subplot()
			#self.axes.plot(x, dataframe[data_visualizer.graph_type(self, tuple_4, self.figure_4)])
			graph(self.graph_4[-1], x, dataframe[data_visualizer.graph_type(self, tuple_4, self.figure_4)])
			self.figure_canvas_4.mpl_connect("button_press_event", lambda event: self.right_popup(event, 4))
			self.axes.set_xticks(self.axes.get_xticks()[::(round(len(x)/3))])

		if len(list)>5:
			tuple_5=(list[0],list[5])
			self.figure_canvas_5 = FigureCanvasTkAgg(self.figure_5, self.sidebar_frame_2)
			#self.figure_canvas_5.graph = [0]
			self.figure_canvas_5.get_tk_widget().grid(row=5, column=3, padx=5, pady=5, sticky="nsw")
			self.axes = self.figure_5.add_subplot()
			#self.axes.plot(x, dataframe[data_visualizer.graph_type(self, tuple_5, self.figure_5)])
			graph(self.graph_5[-1], x, dataframe[data_visualizer.graph_type(self, tuple_5, self.figure_5)])
			self.figure_canvas_5.mpl_connect("button_press_event", lambda event: self.right_popup(event, 5))
			self.axes.set_xticks(self.axes.get_xticks()[::(round(len(x)/3))])

		if len(list)>6:
			tuple_6=(list[0],list[6])
			self.figure_canvas_6 = FigureCanvasTkAgg(self.figure_6, self.sidebar_frame_2)
			#self.figure_canvas_6.graph = [0]
			self.figure_canvas_6.get_tk_widget().grid(row=6, column=3, padx=5, pady=5, sticky="nsw")
			self.axes = self.figure_6.add_subplot()
			#self.axes.plot(x, dataframe[data_visualizer.graph_type(self, tuple_6, self.figure_6)])
			graph(self.graph_6[-1], x, dataframe[data_visualizer.graph_type(self, tuple_6, self.figure_6)])
			self.figure_canvas_6.mpl_connect("button_press_event", lambda event: self.right_popup(event, 6))
			self.axes.set_xticks(self.axes.get_xticks()[::(round(len(x)/3))])

		if len(list)>7:
			tuple_7=(list[0],list[7])
			self.figure_canvas_7 = FigureCanvasTkAgg(self.figure_7, self.sidebar_frame_2)
			#self.figure_canvas_7.graph = [0]
			self.figure_canvas_7.get_tk_widget().grid(row=7, column=3, padx=5, pady=5, sticky="nsw")
			self.axes = self.figure_7.add_subplot()
			#self.axes.plot(x, dataframe[data_visualizer.graph_type(self, tuple_7, self.figure_7)])
			graph(self.graph_7[-1], x, dataframe[data_visualizer.graph_type(self, tuple_7, self.figure_7)])
			self.figure_canvas_7.mpl_connect("button_press_event", lambda event: self.right_popup(event, 7))
			self.axes.set_xticks(self.axes.get_xticks()[::(round(len(x)/3))])

	def sidebar_clear_button(self, start, end, subject, list):
		print("Clear button clicked")
		self.combobox1.set("Summary")
		self.combobox2.set("Subjects")
		self.combobox3.set("Time Start")
		self.combobox4.set("Time Finish")
		self.combobox5.set("Day")
		self.combobox6.set("Day")
		self.checkbox1.deselect()
		self.checkbox2.deselect()
		self.checkbox3.deselect()
		self.checkbox4.deselect()
		self.checkbox5.deselect()
		self.checkbox6.deselect()
		self.checkbox7.deselect()
		self.checkbox8.deselect()
		self.checkbox9.deselect()
		self.figure_1.clear()
		self.figure_2.clear()
		self.figure_3.clear()
		self.figure_4.clear()
		self.figure_5.clear()
		self.figure_6.clear()
		self.figure_7.clear()
		self.figure_canvas_1.draw()
		self.figure_canvas_2.draw()
		self.figure_canvas_3.draw()
		self.figure_canvas_4.draw()
		self.figure_canvas_5.draw()
		self.figure_canvas_6.draw()
		self.figure_canvas_7.draw()

if __name__ == "__main__":
	app = App()
	app.mainloop()