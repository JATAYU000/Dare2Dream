import json
import os
import numpy as np
from motorlib.motor import Motor
from motorlib.grains.bates import BatesGrain
# from motorlib.grains.finocyl import Finocyl
# from motorlib.grains.rodTube import RodTubeGrain
from motorlib.propellant import Propellant
import subprocess

class MotorConfigGenerator:
    def __init__(self, output_dir="generated_data"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "ric"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "csv"), exist_ok=True)

    def generate_propellant(self):
        """Generate random propellant properties"""
        propellant = Propellant()
        propellant.setProperties({
            'name': 'Generated Propellant',
            'density': np.random.uniform(1500, 2000),  # kg/m^3
            'tabs': [{
                'minPressure': 0.1e6,  # 0.1 MPa
                'maxPressure': 10e6,   # 10 MPa
                'a': np.random.uniform(1e-5, 1e-4),  # Burn rate coefficient
                'n': np.random.uniform(0.3, 0.5),     # Burn rate exponent
                'k': np.random.uniform(1.1, 1.3),     # Specific heat ratio
                't': np.random.uniform(2000, 3500),   # Combustion temperature (K)
                'm': np.random.uniform(20, 30)        # Molar mass (g/mol)
            }]
        })
        return propellant

    def generate_bates_grain(self):
        """Generate a BATES grain with random dimensions"""
        grain = BatesGrain()
        diameter = np.random.uniform(0.05, 0.15)  # m
        grain.setProperties({
            'diameter': diameter,
            'length': np.random.uniform(0.1, 0.3),    # m
            'coreDiameter': diameter * np.random.uniform(0.3, 0.7),  # m
            'inhibitedEnds': 'Neither'
        })
        return grain

    def generate_motor_config(self, id_num):
        """Generate a complete motor configuration"""
        motor = Motor()
        
        # Add propellant
        motor.propellant = self.generate_propellant()
        
        # Add grains (1-3 BATES grains)
        num_grains = np.random.randint(1, 4)
        for _ in range(num_grains):
            motor.grains.append(self.generate_bates_grain())
            
        # Configure nozzle
        throat_diameter = np.random.uniform(0.01, 0.03)  # m
        motor.nozzle.setProperties({
            'throat': throat_diameter,
            'exit': throat_diameter * np.random.uniform(1.5, 3.0),
            'efficiency': np.random.uniform(0.85, 0.95),
            'divergenceAngle': np.random.uniform(12, 18),
            'throatLength': throat_diameter * np.random.uniform(0.5, 1.5)
        })

        # Save configuration
        ric_path = os.path.join(self.output_dir, "ric", f"motor_{id_num}.ric")
        csv_path = os.path.join(self.output_dir, "csv", f"motor_{id_num}.csv")
        
        with open(ric_path, 'w') as f:
            json.dump(motor.getDict(), f)
            
        return ric_path, csv_path

    def generate_dataset(self, num_samples):
        """Generate multiple motor configurations and simulate them"""
        print(f"Generating {num_samples} motor configurations...")
        
        for i in range(num_samples):
            print(f"Generating motor {i+1}/{num_samples}")
            ric_path, csv_path = self.generate_motor_config(i)
            
            # Run simulation using CLI
            cmd = ["python", "main.py", ric_path, "-o", csv_path]
            try:
                subprocess.run(cmd, check=True)
                print(f"Successfully simulated motor {i+1}")
            except subprocess.CalledProcessError:
                print(f"Failed to simulate motor {i+1}")
                continue

if __name__ == "__main__":
    generator = MotorConfigGenerator()
    generator.generate_dataset(num_samples=100)  # Generate 100 different motors