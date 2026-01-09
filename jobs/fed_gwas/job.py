# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This code show to use NVIDIA FLARE Job Recipe to connect both Federated learning client and server algorithm
and run it under different environments
"""
import argparse
import os
import subprocess
import numpy as np
import pandas as pd
from nvflare.app_opt.pt.recipes.fedavg import FedAvgRecipe
from nvflare.recipe import SimEnv, add_experiment_tracking, ProdEnv

from nvflare.app_common.aggregators.model_aggregator import ModelAggregator
from nvflare.client import FLModel

from regenie2gwama import regenie2gwama


class GWASMetaAggregator(ModelAggregator):
    """
    Collects GWAS summary statistics from clients and performs
    inverse-variance weighted meta-analysis during aggregation.
    """

    def __init__(self, output_dir="./server_results"):
        super().__init__()
        self.client_betas = []
        self.client_ses = []
        self.received_params_type = None
        self.output_dir = output_dir
        self.gwama_input_file = os.path.join(self.output_dir, "gwama.in")
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize gwama.in file (clear it if it exists)
        with open(self.gwama_input_file, 'w') as f:
            f.write("")  # Clear the file
        
        print(f"GWASMetaAggregator initialized. Results will be saved to: {self.output_dir}")
        print(f"GWAMA input file will be created at: {self.gwama_input_file}")

    def accept_model(self, model: FLModel):
        """
        Called once per client.
        Expects model.params to contain GWAS summary statistics.
        Also saves the results_file from metadata to disk.
        """
        if self.received_params_type is None:
            self.received_params_type = model.params_type

        params = model.params
        
        # Check if this is an error response
        if params.get("SUCCESS") == False:
            site_name = model.meta.get("site_name", "unknown_site")
            error_msg = model.meta.get("error_message", "Unknown error")
            print(f"ERROR: Client {site_name} failed with error: {error_msg}")
            return
        
        # Extract metadata
        site_name = model.meta.get("site_name", "unknown_site")
        dataset_id = model.meta.get("dataset_id", "unknown_id")
        results_file_content = model.meta.get("results_file", "")
        
        # Save the regenie results file to disk
        if results_file_content:
            output_filename = f"site{dataset_id}_{site_name}_regenie_step2_Phen1.regenie"
            output_path = os.path.join(self.output_dir, output_filename)
            
            with open(output_path, 'w') as f:
                f.write(results_file_content)
            
            print(f"Saved results from {site_name} (site{dataset_id}) to: {output_path}")
            print(f"File size: {len(results_file_content)} bytes")
            
            # Convert regenie format to GWAMA format
            gwama_filename = f"site{dataset_id}_{site_name}_gwama.txt"
            gwama_path = os.path.join(self.output_dir, gwama_filename)
            
            try:
                regenie2gwama(output_path, gwama_path, mode='or')
                print(f"Converted to GWAMA format: {gwama_path}")
                
                # Append the GWAMA file path to gwama.in
                with open(self.gwama_input_file, 'a') as f:
                    f.write(f"{gwama_path}\n")
                print(f"Added {gwama_path} to {self.gwama_input_file}")
                
                # Read beta and se from the GWAMA file for meta-analysis
                gwama_df = pd.read_csv(gwama_path, sep="\t")
                beta = gwama_df['BETA'].values
                se = gwama_df['SE'].values
                
                self.client_betas.append(beta)
                self.client_ses.append(se)
                print(f"Extracted {len(beta)} variants with BETA and SE for meta-analysis")
                
            except Exception as e:
                print(f"ERROR: Failed to convert {site_name} results to GWAMA format: {e}")
        else:
            print(f"WARNING: No results_file content received from {site_name}")


    def aggregate_model(self) -> FLModel:
        """
        Perform inverse-variance weighted GWAS meta-analysis.
        """
        betas = np.stack(self.client_betas, axis=0)  # (K, P)
        ses = np.stack(self.client_ses, axis=0)      # (K, P)

        variances = ses ** 2
        weights = 1.0 / variances

        # Meta-analysis estimates
        meta_beta = np.sum(weights * betas, axis=0) / np.sum(weights, axis=0)
        meta_var = 1.0 / np.sum(weights, axis=0)
        meta_se = np.sqrt(meta_var)

        aggregated_params = {
            "beta": meta_beta,
            "se": meta_se,
        }

        print(f"Aggregated beta: {meta_beta}")
        print(f"Aggregated se: {meta_se}")

        # RUN GWAMA
        # Meta-analysis using GWAMA
        gwama_executable = "/home/ubuntu/GWAMA/GWAMA"
        gwama_output_prefix = os.path.join(self.output_dir, "gwama")
        
        gwama_cmd = [
            gwama_executable,
            "-i", self.gwama_input_file,
            "--output", gwama_output_prefix,
            "--name_marker", "MARKERNAME",
            "--name_ea", "EA",
            "--name_nea", "NEA",
            "--name_or", "OR",
            "--name_or_95l", "OR_95L",
            "--name_or_95u", "OR_95U"
        ]
        
        print(f"Running GWAMA meta-analysis...")
        print(f"Command: {' '.join(gwama_cmd)}")
        print(f"Working directory: {os.getcwd()}")
        print(f"Input file: {self.gwama_input_file}")
        
        result = subprocess.run(gwama_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"GWAMA completed successfully")
            print(f"Output files should be at: {gwama_output_prefix}.*")
        else:
            print(f"GWAMA failed with return code: {result.returncode}")
        
        print(f"GWAMA stdout:\n{result.stdout}")
        if result.stderr:
            print(f"GWAMA stderr:\n{result.stderr}")

        return FLModel(
            params=aggregated_params,
            params_type=self.received_params_type,
        )

    def reset_stats(self):
        """
        Clear state between FL rounds.
        """
        self.client_betas = []
        self.client_ses = []
        self.received_params_type = None


def define_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_clients", type=int, default=5)
    parser.add_argument("--num_rounds", type=int, default=1)

    return parser.parse_args()


def main():
    args = define_parser()

    n_clients = args.n_clients
    num_rounds = args.num_rounds

    recipe = FedAvgRecipe(
        name="fed_gwas",
        min_clients=n_clients,
        num_rounds=num_rounds,
        train_script="client.py",
        aggregator=GWASMetaAggregator(),
    )
    add_experiment_tracking(recipe, tracking_type="tensorboard")

    # Send the regenie script to all clients
    recipe.job.to_clients("client_regenie.sh")

    # Simulation Environment (FL Server and clients on same NVIDIA Brev instance)
    # env = SimEnv(num_clients=n_clients)
    
    # Production Environment (FL Server on AWS and clients on NVIDIA Brev)
    env = ProdEnv(startup_kit_location="/home/ubuntu/hroth@nvidia.com", username="hroth@nvidia.com")
    
    run = recipe.execute(env)
    print()
    print("Job Status is:", run.get_status())
    print("Result can be found in :", run.get_result())
    print()


if __name__ == "__main__":
    main()
