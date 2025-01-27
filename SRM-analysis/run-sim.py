import sys
import argparse
from motorlib.motor import Motor
from motorlib.units import convert
import json

def run_motor_simulation(input_file, output_file=None):
    """
    Run motor simulation from a .ric file and output results to CSV
    
    Args:
        input_file (str): Path to input .ric file
        output_file (str, optional): Path to output CSV file. If None, prints to stdout
    """
    try:
        # Load the motor configuration from .ric file
        with open(input_file, 'r') as f:
            motor_dict = json.load(f)
            
        # Create and configure motor
        motor = Motor(motor_dict)
        
        # Run simulation
        sim_result = motor.runSimulation()
        
        # Check for errors
        if not sim_result.success:
            print("Simulation failed with errors:", file=sys.stderr)
            for alert in sim_result.getAlertsByLevel(SimAlertLevel.ERROR):
                print(f"Error: {alert.description}", file=sys.stderr)
            sys.exit(1)
            
        # Output results
        csv_data = sim_result.getCSV()
        if output_file:
            with open(output_file, 'w') as f:
                f.write(csv_data)
        else:
            print(csv_data)
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='OpenMotor CLI - Run rocket motor simulations')
    parser.add_argument('input', help='Input .ric file path')
    parser.add_argument('-o', '--output', help='Output CSV file path')
    
    args = parser.parse_args()
    
    run_motor_simulation(args.input, args.output)

if __name__ == '__main__':
    main()