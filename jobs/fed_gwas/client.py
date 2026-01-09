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
client side training scripts
"""

import os
import subprocess

import nvflare.client as flare
from nvflare.client.tracking import SummaryWriter

DATASET_ROOT = "/home/ubuntu/data/data/simulated_sites"

# Mapping of client names to dataset identifiers
dataset_ids = {
    "client1": 1,
    "PrecisionMedicine": 2,
    "JCVI": 3,
    "SeriousElephant": 4,
    "WonkyBanana": 5,
    "indiana_site": 6,
    "wIndy_site_2": 7,
    "nvidia4": 8,
    "nvidia3": 9,
    "nvidia2": 10,  # slow client - 4 CPUs only
    # "nvidia1": 11,  # slow client - Backup
}

def main():
    flare.init()
    sys_info = flare.system_info()
    client_name = sys_info["site_name"]
    client_name = flare.get_site_name()
    print(f"site name: {client_name}")

    dataset_id = dataset_ids[client_name]


    while flare.is_running():
        input_model = flare.receive()
        print(f"site = {client_name}, current_round={input_model.current_round}")

        assert input_model.total_rounds == 1, "Only one round of training is supported!"

        # Check if results already exist
        dataset_path = os.path.join(DATASET_ROOT, f"site{dataset_id}")
        output_file = os.path.join(dataset_path, "regenie_step2_Phen1.regenie")
        
        if os.path.exists(output_file):
            print(f"Output file already exists: {output_file}")
            print("Skipping script execution and using existing results")
        else:
            print(f"Output file not found: {output_file}")
            print("Running regenie script to generate results")
            
            # Run the regenie script for this site
            script_path = os.path.join(".", flare.get_job_id(), f"app_{client_name}", "custom", "client_regenie.sh")

            # Make the script executable if it exists
            if os.path.exists(script_path):
                os.chmod(script_path, 0o755)
                print(f"Made script executable: {script_path}")
            else:
                raise FileNotFoundError(f"Script not found: {script_path}")

            cmd = [script_path, str(dataset_id)]
            print(f"Running command: {cmd}")
            print(f"Current working directory: {os.getcwd()}")
            print(f"Script exists: {os.path.exists(script_path)}")
            print(f"Script is executable: {os.access(script_path, os.X_OK)}")
            print(f"=" * 80)
            print("Starting subprocess.run() - this should BLOCK until complete...")
            result = subprocess.run(cmd, check=False)
            print("subprocess.run() returned - script has completed")
            print(f"=" * 80)
            print(f"Script completed with return code: {result.returncode}")

            if result.returncode != 0:
                print(f"Error running {script_path}, return code: {result.returncode}")
                return flare.FLModel(
                    params={"SUCCESS": False},
                    meta={
                        "error_message": f"Error running {script_path}, return code: {result.returncode}"
                    }
                )
        
        print(f"Loading results from {output_file}")
        with open(output_file, 'r') as f:
            results_content = f.read()
        
        # Wrap the results in an FLModel and send back to server
        output_model = flare.FLModel(
            params={"SUCCESS": True},
            meta={
                "results_file": results_content,
                "site_name": client_name,
                "dataset_id": dataset_id
            }
        )
        print(f"site: {client_name}, sending results to server.")
        flare.send(output_model)

if __name__ == "__main__":
    main()
