import gradio as gr
import torch
import numpy as np
import os
import sys
import tempfile
import json
import subprocess
import shutil

def run_design(pdb_file, temperature, num_sequences, seed, design_na_only):
    """Run NA-MPNN in design mode using the inference script"""
    try:
        # Create temporary directory for output
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Copy PDB file to temp location
            pdb_path = pdb_file.name
            
            # Set model parameters based on mode
            checkpoint_path = "./models/design_model/s_19137.pt"
            
            # Build command
            cmd = [
                "python", "inference/run.py",
                "--model_type", "na_mpnn",
                "--mode", "design",
                "--checkpoint_na_mpnn", checkpoint_path,
                "--pdb_path", pdb_path,
                "--out_folder", tmp_dir,
                "--temperature", str(temperature),
                "--batch_size", str(num_sequences),
                "--seed", str(seed),
                "--output_pdbs", "0",
                "--output_sequences", "1",
                "--output_specificity", "0"
            ]
            
            if design_na_only:
                cmd.extend(["--design_na_only", "1"])
            
            # Run inference
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                return f"Error running inference:\n{result.stderr}"
            
            # Read output sequences
            seq_dir = os.path.join(tmp_dir, "seqs")
            if os.path.exists(seq_dir):
                fasta_files = [f for f in os.listdir(seq_dir) if f.endswith('.fa')]
                if fasta_files:
                    fasta_path = os.path.join(seq_dir, fasta_files[0])
                    with open(fasta_path, 'r') as f:
                        sequences = f.read()
                    
                    # Add legend
                    legend = "\n\n## Sequence Legend:\n"
                    legend += "Protein residues: A, R, N, D, C, Q, E, G, H, I, L, K, M, F, P, S, T, W, Y, V\n"
                    legend += "DNA residues: a (DA), c (DC), g (DG), t (DT)\n"
                    legend += "RNA residues: b (A), d (C), h (G), u (U)\n"
                    legend += "Unknown: X (protein), x (DNA), y (RNA)\n"
                    
                    return sequences + legend
                else:
                    return "No sequence files generated."
            else:
                return "Output directory not created. Check if inference completed successfully."
            
    except subprocess.TimeoutExpired:
        return "Error: Inference timed out after 5 minutes."
    except Exception as e:
        return f"Error during design: {str(e)}"

def run_specificity(pdb_file, design_na_only):
    """Run NA-MPNN in specificity prediction mode using the inference script"""
    try:
        # Create temporary directory for output
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Copy PDB file to temp location
            pdb_path = pdb_file.name
            
            # Set model parameters based on mode
            checkpoint_path = "./models/specificity_model/s_70114.pt"
            
            # Build command - for specificity, omit amino acids
            cmd = [
                "python", "inference/run.py",
                "--model_type", "na_mpnn",
                "--mode", "specificity",
                "--checkpoint_na_mpnn", checkpoint_path,
                "--pdb_path", pdb_path,
                "--out_folder", tmp_dir,
                "--output_pdbs", "0",
                "--output_sequences", "0",
                "--output_specificity", "1",
                "--omit_AA", "ARNDCQEGHILKMFPSTWYVX"
            ]
            
            if design_na_only:
                cmd.extend(["--design_na_only", "1"])
            
            # Run inference
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                return f"Error running inference:\n{result.stderr}"
            
            # Read specificity output
            spec_dir = os.path.join(tmp_dir, "specificity")
            if os.path.exists(spec_dir):
                npz_files = [f for f in os.listdir(spec_dir) if f.endswith('.npz')]
                if npz_files:
                    npz_path = os.path.join(spec_dir, npz_files[0])
                    specificity_output = np.load(npz_path, allow_pickle=True)
                    
                    # Load useful arrays from the npz file
                    predicted_ppm = specificity_output["predicted_ppm"]
                    dna_mask = specificity_output["dna_mask"].astype(bool)
                    restype_to_int = specificity_output["restype_to_int"].item()
                    
                    residues_to_consider = [
                        restype_to_int["DA"],
                        restype_to_int["DC"],
                        restype_to_int["DG"],
                        restype_to_int["DT"],
                    ]
                    
                    # Subset the PPM
                    predicted_ppm_dna = predicted_ppm[dna_mask][:, residues_to_consider]
                    
                    # Format output
                    output = "## Predicted DNA Position Probability Matrix (PPM)\n\n"
                    output += "Position | DA | DC | DG | DT\n"
                    output += "---------|----|----|----|----|----\n"
                    
                    for i, probs in enumerate(predicted_ppm_dna):
                        output += f"{i+1} | {probs[0]:.4f} | {probs[1]:.4f} | {probs[2]:.4f} | {probs[3]:.4f}\n"
                    
                    output += f"\n\nTotal DNA positions: {len(predicted_ppm_dna)}\n"
                    
                    return output
                else:
                    return "No specificity files generated."
            else:
                return "Output directory not created. Check if inference completed successfully."
            
    except subprocess.TimeoutExpired:
        return "Error: Inference timed out after 5 minutes."
    except Exception as e:
        return f"Error during specificity prediction: {str(e)}"

# Create Gradio interface
with gr.Blocks(title="NA-MPNN: Protein-Nucleic Acid Design and Specificity Prediction") as demo:
    gr.Markdown("""
    # NA-MPNN: Protein-Nucleic Acid Design and Specificity Prediction
    
    This tool allows you to:
    1. **Design** protein and/or nucleic acid sequences given a backbone structure
    2. **Predict specificity** of protein-DNA interactions
    
    Upload a PDB file and choose your mode of operation.
    """)
    
    with gr.Tab("Design Mode"):
        gr.Markdown("""
        ### Design sequences for protein-nucleic acid complexes
        Upload a PDB file containing the backbone structure, and the model will generate designed sequences.
        """)
        
        with gr.Row():
            with gr.Column():
                design_pdb = gr.File(label="Upload PDB File", file_types=[".pdb"])
                design_temperature = gr.Slider(0.05, 1.0, value=0.1, step=0.05, label="Sampling Temperature")
                design_num_seq = gr.Slider(1, 10, value=3, step=1, label="Number of Sequences to Generate")
                design_seed = gr.Number(value=42, label="Random Seed", precision=0)
                design_na_only = gr.Checkbox(label="Design Nucleic Acids Only (keep protein fixed)", value=False)
                design_button = gr.Button("Run Design", variant="primary")
            
            with gr.Column():
                design_output = gr.Textbox(label="Designed Sequences", lines=20)
        
        design_button.click(
            fn=run_design,
            inputs=[design_pdb, design_temperature, design_num_seq, design_seed, design_na_only],
            outputs=design_output
        )
        
        gr.Markdown("""
        ### Examples
        Try these example PDB files:
        - `inference/examples/4oqu.pdb` - Protein-DNA complex
        - `inference/examples/1am9.pdb` - Protein-DNA complex for specificity
        """)
    
    with gr.Tab("Specificity Mode"):
        gr.Markdown("""
        ### Predict DNA binding specificity
        Upload a PDB file containing a protein-DNA complex, and the model will predict the position probability matrix (PPM) for DNA binding.
        """)
        
        with gr.Row():
            with gr.Column():
                spec_pdb = gr.File(label="Upload PDB File", file_types=[".pdb"])
                spec_na_only = gr.Checkbox(label="Predict for Nucleic Acids Only", value=True)
                spec_button = gr.Button("Run Specificity Prediction", variant="primary")
            
            with gr.Column():
                spec_output = gr.Textbox(label="Predicted Specificity (PPM)", lines=20)
        
        spec_button.click(
            fn=run_specificity,
            inputs=[spec_pdb, spec_na_only],
            outputs=spec_output
        )
    
    with gr.Tab("About"):
        gr.Markdown("""
        ## About NA-MPNN
        
        NA-MPNN (Nucleic Acid Message Passing Neural Network) is a deep learning model for:
        - Designing protein and nucleic acid sequences for given backbone structures
        - Predicting protein-DNA binding specificity
        
        ### Citation
        If you use NA-MPNN in your research, please cite the appropriate paper.
        
        ### Model Information
        - **Architecture**: Message Passing Neural Network (MPNN)
        - **Input**: PDB structure files containing protein-nucleic acid complexes
        - **Output**: 
          - Design mode: Designed sequences in FASTA format
          - Specificity mode: Position Probability Matrix (PPM) for DNA binding
        
        ### Residue Encoding
        The model uses a non-standard one-letter alphabet:
        - **Protein**: Standard amino acid codes (A, R, N, D, C, Q, E, G, H, I, L, K, M, F, P, S, T, W, Y, V)
        - **DNA**: Lowercase letters (a=DA, c=DC, g=DG, t=DT)
        - **RNA**: Special letters (b=A, d=C, h=G, u=U)
        
        ### Repository
        [https://github.com/baker-laboratory/NA-MPNN](https://github.com/baker-laboratory/NA-MPNN)
        """)

if __name__ == "__main__":
    demo.launch()
