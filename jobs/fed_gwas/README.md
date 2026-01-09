
# FedGen: Federated GWAS & GWAMA

Install the dependencies:

```
  pip install -r requirements.txt
```

## Code Structure

``` bash
    fed_gwas
    |
    |-- client.py             # client local training script
    |-- model.py              # model definition
    |-- job.py                # job recipe that defines client and server configurations
    |-- requirements.txt      # dependencies
```

## Running the Job

The `job.py` script orchestrates the federated GWAS analysis across multiple clients. It collects GWAS summary statistics from each client and performs inverse-variance weighted meta-analysis using GWAMA.

### Basic Usage

```bash
python job.py --n_clients <number_of_clients> --num_rounds <number_of_rounds>
```

### Command-Line Arguments

- `--n_clients`: Number of federated learning clients to participate (default: 10)
- `--num_rounds`: Number of federated learning rounds to execute (default: 1)
- `--env`: Environment to run in: `sim` for SimEnv or `prod` for ProdEnv (default: `prod`)
  - **SimEnv**: Simulation environment where FL server and clients run on the same machine
  - **ProdEnv**: Production environment for distributed deployment (e.g., server on AWS, clients on NVIDIA instances)
- `--startup_kit`: Startup kit location for ProdEnv (default: `/home/ubuntu/hroth@nvidia.com`)
- `--username`: Username for ProdEnv (default: `hroth@nvidia.com`)

### Examples

```bash
# Run in simulation environment with 5 clients for 1 round
python job.py --env sim --n_clients 5 --num_rounds 1

# Run in production environment with default settings
python job.py --env prod --n_clients 10 --num_rounds 1

# Run in production environment with custom startup kit and username
python job.py --env prod --startup_kit /path/to/startup_kit --username user@example.com

# Run with default settings (production environment, 10 clients, 1 round)
python job.py
```

### Prerequisites

1. **GWAMA executable**: The GWAMA meta-analysis tool must be installed at `/home/ubuntu/GWAMA/GWAMA` on the server. See [here](../../scripts/run_gwama/README.md).
2. **NVIDIA FLARE startup kit**: Required for production environment deployment (configured in `job.py`)
3. **Client data**: Each client will compute REGENIE output files if they don't already exists.

### What the Job Does

1. Distributes the `client.py` script and `client_regenie.sh` to all federated clients
2. Each client performs local GWAS analysis using REGENIE (if output files don't exist yet)
3. Clients send summary statistics files (including BETA, SE, OR) back to the server
4. Server aggregates results using:
   - Optional simple inverse-variance weighted meta-analysis (Python-based)
   - GWAMA meta-analysis (comprehensive results)
5. Final meta-analysis results are saved to `server_results/` directory

### Output

Results are stored in the job's run directory under `server_results/`:
- Individual client REGENIE files: `site{id}_{name}_regenie_step2_Phen1.regenie`
- GWAMA format files: `site{id}_{name}_gwama.txt`
- GWAMA input list: `gwama.in`
- GWAMA meta-analysis results: `gwama.*` files
