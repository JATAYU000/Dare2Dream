import json
import os
import numpy as np
from motorlib.motor import Motor
from motorlib.grains.bates import BatesGrain
from motorlib.grains.finocyl import FinocylGrain
from motorlib.grains.rodTube import RodTubeGrain
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
            'density': np.random.uniform(1600, 1900),  # kg/m^3
            'tabs': [{
                'minPressure': 0.5e6,  # 0.5 MPa
                'maxPressure': 10e6,   # 10 MPa
                'a': np.random.uniform(1e-5, 5e-5),  # Burn rate coefficient
                'n': np.random.uniform(0.3, 0.4),     # Burn rate exponent
                'k': np.random.uniform(1.2, 1.3),     # Specific heat ratio
                't': np.random.uniform(2500, 3300),   # Combustion temperature (K)
                'm': np.random.uniform(20, 30)        # Molar mass (g/mol)
            }]
        })
        return propellant

    def generate_grain(self, grain_type):
        """Generate a grain with random dimensions based on the type"""
        if grain_type == "BATES":
            grain = BatesGrain()
            diameter = np.random.uniform(0.05, 0.12)  # m
            grain.setProperties({
                'diameter': diameter,
                'length': np.random.uniform(0.15, 0.25),  # m
                'coreDiameter': diameter * np.random.uniform(0.3, 0.6),  # m
                'inhibitedEnds': 'Neither'
            })
        elif grain_type == "Finocyl":
            grain = FinocylGrain()
            grain.setProperties({
                'webThickness': np.random.uniform(0.005, 0.02),  # m
                'outerDiameter': np.random.uniform(0.06, 0.1),   # m
                'innerDiameter': np.random.uniform(0.02, 0.04),  # m
                'length': np.random.uniform(0.1, 0.3)            # m
            })
        elif grain_type == "RodTube":
            grain = RodTubeGrain()
            outer_diameter = np.random.uniform(0.06, 0.1)  # m
            grain.setProperties({
                'outerDiameter': outer_diameter,
                'innerDiameter': outer_diameter * np.random.uniform(0.4, 0.6),  # m
                'length': np.random.uniform(0.1, 0.25)                          # m
            })
        else:
            raise ValueError(f"Unknown grain type: {grain_type}")

        return grain

    def generate_motor_config(self, id_num):
        """Generate a complete motor configuration"""
        motor = Motor()

        # Add propellant
        motor.propellant = self.generate_propellant()

        # Add grains (1-3 grains of random types)
        num_grains = np.random.randint(1, 4)
        grain_types = ["BATES", "Finocyl", "RodTube"]
        for _ in range(num_grains):
            grain_type = np.random.choice(grain_types)
            motor.grains.append(self.generate_grain(grain_type))

        # Configure nozzle
        throat_diameter = np.random.uniform(0.01, 0.03)  # m
        motor.nozzle.setProperties({
            'throat': throat_diameter,
            'exit': throat_diameter * np.random.uniform(2.0, 3.5),
            'efficiency': np.random.uniform(0.85, 0.95),
            'divergenceAngle': np.random.uniform(12, 15),
            'throatLength': throat_diameter * np.random.uniform(0.6, 1.2)
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
            cmd = ["python", "run-sim.py", ric_path, "-o", csv_path]
            try:
                subprocess.run(cmd, check=True)
                print(f"Successfully simulated motor {i+1}")
            except subprocess.CalledProcessError:
                print(f"Failed to simulate motor {i+1}")
                continue

if __name__ == "__main__":
    generator = MotorConfigGenerator()
    generator.generate_dataset(num_samples=100)  # Generate 100 different motors
