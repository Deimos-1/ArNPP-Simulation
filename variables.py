from dataclasses import dataclass

# Flags to control the running state
running = True
frozen = False

def on_close():
    global running
    running = False

initial_flux_values : dict = {i : 0 if i <= 0 else None for i in range(-50,11)}
initial_variables : dict = {
    'p': -1, # [Nile]
    'neutron_flux': 0.0, # [%n/m3*s]
    'temperature': 20.0, # [°C]
    'pressure': 150.0,
    'primary_flow': 10_000.0, # [0,16'000] [kg/s]
    #'T_cold': 320 # [°C]
}



@dataclass
class Variables: 
    p: float = 0
    neutron_flux: float = 0
    temperature: float = 0  ## or 'T-hot'
    pressure: float = 0
    primary_flow: float = 0
    #T_cold: float = 0

    ## temporarily simulate other water circuits with a cooling of 80% for Tcold
    @property
    def T_cold(self):
        if 0.8*self.temperature > 20:
            return 0.8*self.temperature
        else: 
            return 20

    @property
    def thermal_power(self):
        return (self.neutron_flux/100)*3000 ## linear relation: 100% neutron flux --> 3000 [MW] thermal power

    @property
    def power_defect(self):
        return self.temperature*64/1000 ## temperature fuel coefficient = -4 mN/°C and moderator temperature coefficient = -60 mN/°C

    def update(self):
        self.neutron_flux += (self.p - self.power_defect) ## the number on the right is the 'amplification factor' 
        if self.neutron_flux < 0: # non-negativity constraint
            self.neutron_flux = 0

        self.temperature = self.T_cold + self.thermal_power*1_000_000/(self.primary_flow*4_180) ## max 3000 MW thermal power --> 350°C with 16'000 [kg/s] of water max
        



# To instantiate an object use: var = Variables(**initial_variables) 

