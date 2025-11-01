# NA-MPNN
## Introduction
This repository holds the training and inference code for NA-MPNN. See below for installation and examples.

## 🚀 Try it on Hugging Face Space
You can now use NA-MPNN directly in your browser without any installation! Visit our Hugging Face Space for an interactive interface:
- **Design Mode**: Generate protein and nucleic acid sequences for backbone structures
- **Specificity Mode**: Predict DNA binding specificity for protein-DNA complexes

Simply upload a PDB file and get results instantly. Perfect for quick experiments and demonstrations!

## Installation
Installation of NA-MPNN should take between 10-30 minutes depending on your system and internet connection. The bulk of the time is spent setting up the conda environment. The inference code has been tested on Linux and Windows operating systems.

The inference code has been tested on a CPU with the following python/module versions:
- Python v3.12.11
- NumPy v2.3.3
- pandas v2.3.2
- ProDy v2.6.1
- OpenBabel v3.1.0
- PyTorch v2.5.1
- CUDA v12.4

### 1. Clone NA-MPNN
```sh
git clone https://github.com/baker-laboratory/NA-MPNN
```

### 2. Environment Setup
```sh
# Create and activate a new conda environment.
conda create -n NA-MPNN -y
conda activate NA-MPNN

# Install dependencies.
conda install \
    -c pytorch \
    -c nvidia \
    -c conda-forge \
    ipykernel \
    openbabel \
    ProDy \
    pyarrow \
    pandas \
    pytorch \
    pytorch-cuda \
    cmake
```

### 3. (Optional) Setup pdbx
Note: this step is only necessary if you want to work with the training code. For inference only, pdbx is not required. As such, the *cmake* dependency in the previous step is also optional if you only want to run inference.

Clone and build pdbx:
```sh
# Change to the NA-MPNN directory.
cd NA-MPNN

# Clone pdbx.
git clone https://github.com/soedinglab/pdbx.git ./pdbx

# Build pdbx.
cmake -S ./pdbx -B ./pdbx/build -DCMAKE_POLICY_VERSION_MINIMUM=3.5
cmake --build ./pdbx/build
```
Add pdbx to your python path:
```sh
# Set the PYTHONPATH environment variable to include pdbx.
conda env config vars set PYTHONPATH="$(pwd)/pdbx"

# Reactivate the conda environment to apply the changes.
conda deactivate && conda activate NA-MPNN
```

## Examples
The following demonstrations should run in less than 1 minute on a CPU.
### Design
```sh
python ./inference/run.py \
    --model_type "na_mpnn" \
    --mode "design" \
    --pdb_path "./inference/examples/4oqu.pdb" \
    --out_folder "./out/design"
```
One of the outputs of the design model is a fasta file containing the designed sequences. A non-standard one letter alphabet is used to represent protein and nucleic acid residues. The mapping from one letter code to residue type is as follows:
```
A: ALA
R: ARG
N: ASN
D: ASP
C: CYS
Q: GLN
E: GLU
G: GLY
H: HIS
I: ILE
L: LEU
K: LYS
M: MET
F: PHE
P: PRO
S: SER
T: THR
W: TRP
Y: TYR
V: VAL
X: UNK
a: DA
c: DC
g: DG
t: DT
x: DX
b: A
d: C
h: G
u: U
y: RX
```

### Specificity
```sh
python ./inference/run.py \
    --model_type "na_mpnn" \
    --mode "specificity" \
    --pdb_path "./inference/examples/1am9.pdb" \
    --out_folder "./out/specificity" \
    --design_na_only 1 \
    --output_pdbs 0 \
    --output_sequences 0 \
    --output_specificity 1 \
    --omit_AA "ARNDCQEGHILKMFPSTWYVX"
```
The `omit_AA` flag is technically optional but is included in this case since we are only making specificity predictions for nucleic acid residues (protein residues are fixed for protein-DNA specificity prediction).

For compatibility reasons, the predicted PPM has "predictions" for all residues (including fixed protein residues). To extract the predicted DNA PPM, you can use the following code snippet:
```python
import numpy as np

specificity_output_path = "./out/specificity/specificity/1am9.npz"
specificity_output = np.load(specificity_output_path, allow_pickle=True)

# Load useful arrays from the npz file.
predicted_ppm = specificity_output["predicted_ppm"]
dna_mask = specificity_output["dna_mask"].astype(bool)
restype_to_int = specificity_output["restype_to_int"].item()

residues_to_consider = [
    restype_to_int["DA"],
    restype_to_int["DC"],
    restype_to_int["DG"],
    restype_to_int["DT"],
]

# Subset the PPM.
predicted_ppm_dna = predicted_ppm[dna_mask][:, residues_to_consider]
```

### For Additional Hyperparameter Options
```sh
python ./inference/run.py --help
```

## GitHub Actions Workflows

This repository includes automated GitHub Actions workflows for running NA-MPNN:

### Inference Workflow (`run-na-mpnn.yml`)
Automatically runs NA-MPNN inference examples on push or can be triggered manually.
- Runs design and specificity modes on example PDB files
- Uploads output artifacts
- Can be customized via manual trigger parameters

### Training Workflow (`run-na-training.yml`)
Runs the NA-MPNN training script (`na_run.py`) with a configuration file.
- Manual trigger only
- Includes test data generation for quick validation
- Configure with custom JSON files for actual training

See [.github/workflows/README.md](.github/workflows/README.md) for detailed documentation.

## Splits
The *splits* folder contains information about the structures and PPM IDs used
for training and evaluation. This includes information on the train/validation/test splits.

## Hugging Face Space Deployment
This repository is set up to run as a Hugging Face Space, providing an easy-to-use web interface for NA-MPNN.

### Files for Hugging Face Space
- `app.py` - Gradio web interface for design and specificity prediction
- `requirements.txt` - Python dependencies for the Space
- `README_HF.md` - Documentation for the Hugging Face Space (with YAML frontmatter)
- `.gitignore` - Excludes temporary files and build artifacts

### Deploying to Hugging Face
To deploy this repository as a Hugging Face Space:

1. **Create a new Space** on Hugging Face:
   - Go to [huggingface.co/new-space](https://huggingface.co/new-space)
   - Select "Gradio" as the SDK
   - Choose your Space name and visibility settings

2. **Connect your repository**:
   ```sh
   git remote add hf https://huggingface.co/spaces/<your-username>/<space-name>
   git push hf main
   ```

3. **Rename README** (on Hugging Face):
   - Rename `README_HF.md` to `README.md` in the Space repository
   - This ensures the YAML frontmatter is recognized

4. **Wait for deployment**:
   - Hugging Face will automatically build and deploy your Space
   - The app will be available at `https://huggingface.co/spaces/<your-username>/<space-name>`

### Using the Gradio Interface
The web interface provides two modes:

**Design Mode:**
- Upload a PDB file containing a backbone structure
- Adjust temperature for sampling diversity
- Set number of sequences to generate
- Option to design only nucleic acids (keep protein fixed)

**Specificity Mode:**
- Upload a PDB file with a protein-DNA complex
- Get Position Probability Matrix (PPM) predictions
- View binding preferences for each DNA position

### Local Testing
To test the Gradio interface locally:
```sh
pip install -r requirements.txt
python app.py
```
Then open your browser to the URL displayed in the terminal (typically http://localhost:7860).