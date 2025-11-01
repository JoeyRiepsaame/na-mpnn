# test_model.json Configuration

This file is a minimal test configuration for the NA-MPNN training workflow.

## Important Notes

### File Paths
The configuration uses **relative paths** that are resolved from the repository root:
- `DF_PATH_TRAIN`: `./data/test_train.csv`
- `DF_PATH_VALID`: `./data/test_valid.csv`
- `BASE_FOLDER`: `./test_output/`

When running the training workflow, ensure you are in the repository root directory, or modify these paths to be absolute.

### Test Data
The training workflow automatically generates minimal test data when using `test_model.json`:
- Creates CSV files with structure paths, assembly IDs, and metadata
- Generates a minimal assembly lengths file (`.npy` format)
- Uses example PDB files from the `inference/examples/` directory

### Configuration Parameters
Key parameters adjusted for quick testing:
- `MAX_NUMBER_OF_PDBS_TRAIN`: 2 (reduced from thousands)
- `MAX_NUMBER_OF_PDBS_VALID`: 1 (reduced from hundreds)
- `TOTAL_STEPS`: 2 (reduced from 100,000)
- `NUM_WORKERS`: 1 (reduced from 12)
- `MIXED_PRECISION`: 0 (disabled for CPU compatibility)

### Real Training
For actual model training, create a custom configuration file:
1. Copy `design_model.json` or `specificity_model.json` as a template
2. Update paths to point to your preprocessed training data
3. Adjust hyperparameters as needed
4. Use the workflow with your custom config file

## Usage with GitHub Actions

Trigger the training workflow with this config:
1. Go to Actions → "Run NA-MPNN Training"
2. Click "Run workflow"
3. Use default config (`test_model.json`) or specify a custom one
4. Review outputs in the workflow artifacts
