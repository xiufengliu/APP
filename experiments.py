import numpy as np
import pandas as pd
from app_model import APPModel
from visualization import Visualizer

class ExperimentRunner:
    def __init__(self):
        self.visualizer = Visualizer()
        
    def run_emission_pattern_analysis(self):
        """Analyze how different emission patterns affect production decisions"""
        model = APPModel()
        results = []
        
        # Test different emission functions across production volumes
        production_levels = np.linspace(50, 250, 20)  # From min to capacity
        emission_types = ['linear', 'quadratic', 'exponential', 'logarithmic']
        
        for func_type in emission_types:
            production_plan, emissions, costs = model.solve(
                emission_type=func_type,
                production_levels=production_levels
            )
            # Calculate total emissions across all scenarios and periods
            total_emissions = np.sum(emissions)
            results.append({
                'function_type': func_type,
                'production_plan': production_plan,
                'emissions': emissions,
                'total_emissions': total_emissions,
                'total_cost': costs['total'],
                'emission_cost': costs['emission'],
                'production_cost': costs['production']
            })
        
        self.visualizer.plot_emission_comparison(pd.DataFrame(results))
        return pd.DataFrame(results)
    def run_industry_case_studies(self):
        """Run case studies for steel and semiconductor industries"""
        # Steel industry parameters
        steel_params = {
            'alpha': 0.15,  # Base emission factor
            'beta': 0.003,  # Quadratic term for increasing emissions
            'capacity': 200,  # Units per period
            'demand_mean': 150,
            'demand_std': 30
        }
        
        # Semiconductor industry parameters
        semi_params = {
            'alpha': 2.0,  # Scaling factor
            'beta': 0.2,   # Rate parameter
            'capacity': 300,
            'demand_mean': 200,
            'demand_std': 40
        }
        
        results = {
            'steel': self.run_industry_scenario('steel', steel_params, 'quadratic'),  # Higher emissions at high production
            'semi': self.run_industry_scenario('semiconductor', semi_params, 'logarithmic')  # Efficiency gains at scale
        }
        
        self.visualizer.plot_industry_comparison(results)
        return results

    def run_sustainability_analysis(self):
        """Analyze trade-offs between economic and environmental objectives"""
        emission_costs = [20, 50, 80]  # $/ton
        emission_caps = [1500, 2000, 2500]  # tons/period
        results = []
        
        for cost in emission_costs:
            for cap in emission_caps:
                for func_type in ['linear', 'quadratic', 'exponential', 'logarithmic']:
                    model = APPModel(emission_cost=cost, emission_cap=cap)
                    total_cost, total_emissions, service_level, avg_inventory = model.solve(emission_type=func_type)
                    
                    results.append({
                        'emission_cost': cost,
                        'emission_cap': cap,
                        'function_type': func_type,
                        'total_cost': total_cost,
                        'total_emissions': total_emissions,
                        'service_level': service_level,
                        'inventory_levels': avg_inventory
                    })
        
        self.visualizer.plot_sustainability_tradeoffs(pd.DataFrame(results))
        return pd.DataFrame(results)

    def run_industry_scenario(self, industry_type, params, emission_type):
        """Run specific industry scenario"""
        # Extract model parameters
        model_params = {
            'emission_cost': params.get('emission_cost', 50),
            'emission_cap': params.get('emission_cap', 2500),
            'demand_uncertainty': params.get('demand_uncertainty', None)
        }
        
        # Create model with proper parameters
        model = APPModel(**model_params)
        
        # Solve the model with the specified emission type
        return model.solve(emission_type=emission_type)

    def analyze_demand_uncertainty(self):
        """Analyze impact of demand uncertainty on emission patterns"""
        uncertainty_levels = [0.1, 0.2, 0.3]  # Coefficient of variation
        results = []
        
        for uncertainty in uncertainty_levels:
            model = APPModel(demand_uncertainty=uncertainty)
            for func_type in ['linear', 'quadratic', 'exponential', 'logarithmic']:
                metrics = model.solve(emission_type=func_type)
                results.append({
                    'uncertainty': uncertainty,
                    'function_type': func_type,
                    'expected_cost': metrics['expected_cost'],
                    'expected_emissions': metrics['expected_emissions'],
                    'cost_variance': metrics['cost_variance'],
                    'emission_variance': metrics['emission_variance']
                })
        
        self.visualizer.plot_uncertainty_analysis(pd.DataFrame(results))
        return pd.DataFrame(results)
    def run_sensitivity_analysis(self):
        """Perform sensitivity analysis"""
        emission_costs = [20, 40, 60, 80]
        results = []
        
        for cost in emission_costs:
            model = APPModel(emission_cost=cost)
            for func_type in ['linear', 'quadratic', 'exponential', 'logarithmic']:
                total_cost, total_emissions = model.solve(emission_type=func_type)
                results.append({
                    'emission_cost': cost,
                    'function_type': func_type,
                    'total_cost': total_cost,
                    'total_emissions': total_emissions
                })
        
        results_df = pd.DataFrame(results)
        self.visualizer.plot_sensitivity_analysis(
            results_df, 
            'emission_cost', 
            'total_cost', 
            'Sensitivity to Emission Costs'
        )