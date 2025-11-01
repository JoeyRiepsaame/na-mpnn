# GitHub Actions Workflows for NA-MPNN

This directory contains GitHub Actions workflows for automating the execution of NA-MPNN models.

## Workflows

### 1. run-na-mpnn.yml - Inference Workflow

**Purpose**: Runs NA-MPNN inference in both design and specificity modes using example PDB files.

**Triggers**:
- Manual trigger via workflow_dispatch (allows custom input parameters)
- Automatic trigger on push to main/master branch when Python files or requirements change

**What it does**:
- Sets up Python 3.8 environment
- Installs required dependencies (OpenBabel, PyTorch, ProDy, etc.)
- Runs design mode inference on example structure (4oqu.pdb)
- Runs specificity mode inference on example structure (1am9.pdb)
- Uploads output artifacts for review

**Manual trigger parameters**:
- `model_type`: Model type (default: "na_mpnn")
- `mode`: Inference mode - "design" or "specificity" (default: "design")
- `pdb_path`: Path to PDB file (default: "./inference/examples/4oqu.pdb")

### 2. run-na-training.yml - Training Workflow

**Purpose**: Runs the NA-MPNN training script (na_run.py) with a specified configuration file.

**Triggers**:
- Manual trigger only via workflow_dispatch

**What it does**:
- Sets up Python 3.8 environment
- Installs required dependencies
- Creates minimal test data if using the test configuration
- Runs na_run.py with specified JSON configuration
- Uploads training outputs and logs

**Manual trigger parameters**:
- `config_file`: Path to JSON configuration file (default: "test_model.json")

**Note**: The training workflow with default test configuration creates minimal synthetic data for testing purposes. For actual training, you need to:
1. Prepare proper training/validation CSV files with preprocessed structure data
2. Create a custom JSON configuration file pointing to your data
3. Manually trigger the workflow with your config file

## Usage

### Running Inference Workflow

**Via GitHub UI**:
1. Go to Actions tab in your repository
2. Select "Run NA-MPNN Model" workflow
3. Click "Run workflow"
4. (Optional) Customize input parameters
5. Click "Run workflow" button

**Example outputs**:
- Design mode: FASTA files with designed sequences
- Specificity mode: NPZ files with predicted PPMs

### Running Training Workflow

**Via GitHub UI**:
1. Go to Actions tab in your repository
2. Select "Run NA-MPNN Training" workflow
3. Click "Run workflow"
4. (Optional) Specify your config file path
5. Click "Run workflow" button

**With custom data**:
1. Prepare your training data (CSV files with structure paths, dates, etc.)
2. Create a JSON config file (see `design_model.json` or `specificity_model.json` as examples)
3. Commit both to your repository
4. Manually trigger the workflow with your config file path

## Requirements

The workflows automatically install dependencies from `requirements.txt`, which includes:
- numpy
- pandas
- torch
- openbabel
- ProDy
- pyarrow

## Outputs

All workflows upload artifacts that are retained for 7 days:
- Inference outputs (sequences, structures, PPMs)
- Training outputs (model checkpoints, logs)

Access artifacts via the workflow run summary page in the Actions tab.
