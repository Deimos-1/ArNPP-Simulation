import tkinter as tk
import matplotlib.pyplot as plt
import sys
from dataclasses import dataclass, field
from variables import Variables, on_close
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

@dataclass
class GUI():
    title: str = 'ArNPP Neutronic simulation'
    width: int = 1000
    height: int = 700
    bg_color: str = "white"
    variable: Variables = field(default_factory=Variables)


    ## Persistent StringVar
    reactivity_txt: tk.StringVar = field(init=False, repr=False)
    flux_txt: tk.StringVar = field(init=False, repr=False) 
    temperature_txt: tk.StringVar = field(init=False, repr=False) 
    thermal_power_txt: tk.StringVar = field(init=False, repr=False) 
    primary_flow_txt: tk.StringVar = field(init=False, repr=False)

    ## for the plot
    fig: Figure = None
    anim: FuncAnimation = None
    window: tk.Tk = field(init=False, repr=False)

    upper_frame: tk.Frame = field(init=False, repr=False)
    row1_frame: tk.Frame = field(init=False, repr=False)
    row2_frame: tk.Frame = field(init=False, repr=False)
    remaining_rows_frame: tk.Frame = field(init=False, repr=False)
    

    def reactivity_raise(self):
        self.variable.p += 0.01 ## initialy 0.001
        self.reactivity_txt.set(f"Reactivity: {self.variable.p:.2f} [N]")

    def reactivity_lower(self):
        self.variable.p -= 0.01 ## initialy 0.001
        self.reactivity_txt.set(f"Reactivity: {self.variable.p:.2f} [N]")

    def reactivity_raise_big(self):
        self.variable.p += 0.1
        self.reactivity_txt.set(f"Reactivity: {self.variable.p:.2f} [N]")

    def reactivity_lower_big(self):
        self.variable.p -= 0.1 
        self.reactivity_txt.set(f"Reactivity: {self.variable.p:.2f} [N]")    

    def primary_flow_raise(self):
        self.variable.primary_flow += 100 ## arbitrary, in the cr, it will be set via command in 
        self.primary_flow_txt.set(f"Primary Water Flow: {self.variable.primary_flow:.0f} [L/s]")

    def primary_flow_lower(self):
        self.variable.primary_flow -= 100 ## arbitrary, in the cr, it will be set via command in 
        self.primary_flow_txt.set(f"Primary Water Flow: {self.variable.primary_flow:.0f} [L/s]")


    def update_indicators(self):  # <-- New method
        """
        Periodically update the indicators to reflect changes in the Variables instance.
        """
        # Update each StringVar with the latest values
        self.reactivity_txt.set(f"Reactivity: {self.variable.p:.2f} [N]")
        self.flux_txt.set(f"Neutron Flux: {self.variable.neutron_flux:.1f} [%]")
        self.temperature_txt.set(f"Temperature: {self.variable.temperature:.0f} [°C]")
        self.thermal_power_txt.set(f"Thermal Power: {self.variable.thermal_power:.0f} [MW]")
        self.primary_flow_txt.set(f"Primary Water Flow: {self.variable.primary_flow:.0f} [L/s]")

        # Schedule the next update after 100 ms (10fps)
        self.window.after(100, self.update_indicators)


    def __post_init__(self, ):
        # Initialize the Tkinter window
        self.window = tk.Tk()
        self.window.title(self.title)
        self.window.geometry(f"{self.width}x{self.height}+500+50")
        self.window.configure(bg=self.bg_color)

        ## Frames
        self.upper_frame = tk.Frame(self.window)
        self.row1_frame = tk.Frame(self.upper_frame)
        self.row2_frame = tk.Frame(self.upper_frame)
        self.remaining_rows_frame = tk.Frame(self.upper_frame)


        ## Text variables
        self.reactivity_txt = tk.StringVar(master=self.row1_frame, value=f"Reactivity: {self.variable.p:.2f} [N]")
        self.flux_txt = tk.StringVar(master=self.row2_frame, value=f"Neutron Flux: {self.variable.neutron_flux:.1f} [%]")
        self.temperature_txt = tk.StringVar(master=self.remaining_rows_frame, value=f"Temperature: {self.variable.temperature:.0f} [°C]")
        self.thermal_power_txt = tk.StringVar(master=self.remaining_rows_frame, value=f"Thermal Power: {self.variable.thermal_power:.0f} [MW]")
        self.primary_flow_txt = tk.StringVar(master=self.remaining_rows_frame, value=f"Primary Water Flow: {self.variable.primary_flow:.0f} [L/s]")


        ## Buttons
        button_reactivity_raise = tk.Button(master=self.row1_frame, text='+', command=self.reactivity_raise)
        button_reactivity_decrease = tk.Button(master=self.row1_frame, text='-', command=self.reactivity_lower)
        button_reactivity_raise_big = tk.Button(master=self.row1_frame, text='++', command=self.reactivity_raise_big)
        button_reactivity_decrease_big = tk.Button(master=self.row1_frame, text='--', command=self.reactivity_lower_big)
        button_primary_flow_raise = tk.Button(master=self.row2_frame, text='+', command=self.primary_flow_raise)
        button_primary_flow_lower = tk.Button(master=self.row2_frame, text='-', command=self.primary_flow_lower)


        ## Text displays
        reactivity_indicator = tk.Label(master=self.row1_frame, textvariable=self.reactivity_txt)
        primary_flow_indicator = tk.Label(master=self.row2_frame, textvariable=self.primary_flow_txt)
        flux_indicator = tk.Label(master=self.remaining_rows_frame, textvariable=self.flux_txt)
        temperature_indicator = tk.Label(master=self.remaining_rows_frame, textvariable=self.temperature_txt)
        thermal_power_indicator = tk.Label(master=self.remaining_rows_frame, textvariable=self.thermal_power_txt)


        ## Packing row1_frame
        reactivity_indicator.pack(side='left')
        button_reactivity_raise_big.pack(side='left')
        button_reactivity_raise.pack(side='left')
        button_reactivity_decrease.pack(side='left')
        button_reactivity_decrease_big.pack(side='left')
        
        ## Packing row2_frame
        primary_flow_indicator.pack(side='left')
        button_primary_flow_raise.pack(side='left')
        button_primary_flow_lower.pack(side='left')
        
        ## Packing remaining_rows_frame
        flux_indicator.pack()
        temperature_indicator.pack()
        thermal_power_indicator.pack()

        ## Packing global frames
        self.row1_frame.pack(padx=0)
        self.row2_frame.pack(padx=0)
        self.remaining_rows_frame.pack(padx=0)
        self.upper_frame.pack(side='top')

        # Embed the Matplotlib figure in Tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, # fill=tk.BOTH,
                                          expand=True)

        self.window.bind("<Destroy>", lambda f: sys.exit()) ## make the program stop if the window closes
        # Start updating indicators
        self.update_indicators()

    def start(self):
        # Run the Tkinter main loop
        self.window.mainloop()

