---
title: NA-MPNN
emoji: 🧬
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.5.0
app_file: app.py
pinned: false
license: apache-2.0
---

# NA-MPNN: Protein-Nucleic Acid Design and Specificity Prediction

This is a Hugging Face Space for NA-MPNN, a deep learning model for designing protein and nucleic acid sequences and predicting protein-DNA binding specificity.

## What is NA-MPNN?

NA-MPNN (Nucleic Acid Message Passing Neural Network) is a state-of-the-art deep learning model that can:

1. **Design sequences** for protein-nucleic acid complexes given a backbone structure
2. **Predict binding specificity** for protein-DNA interactions

## How to Use This Space

### Design Mode
1. Upload a PDB file containing a protein-nucleic acid complex backbone structure
2. Adjust the temperature (controls diversity of designs, lower = more conservative)
3. Set the number of sequences to generate
4. Optionally set a random seed for reproducibility
5. Choose whether to design only nucleic acids (keeping protein fixed) or design both
6. Click "Run Design" to generate designed sequences

### Specificity Mode
1. Upload a PDB file containing a protein-DNA complex
2. Click "Run Specificity Prediction" to get the Position Probability Matrix (PPM)
3. The output shows the predicted binding preferences for each DNA position

## Example Files

The Space includes example PDB files you can download and test:
- `inference/examples/4oqu.pdb` - A protein-DNA complex suitable for design
- `inference/examples/1am9.pdb` - A protein-DNA complex suitable for specificity prediction

## Sequence Encoding

The model uses a special one-letter alphabet to represent residues:
- **Protein residues**: Standard amino acid codes (A, R, N, D, C, Q, E, G, H, I, L, K, M, F, P, S, T, W, Y, V, X)
- **DNA residues**: Lowercase letters (a=DA, c=DC, g=DG, t=DT, x=DX)
- **RNA residues**: Special letters (b=A, d=C, h=G, u=U, y=RX)

## Model Information

- **Architecture**: Message Passing Neural Network (MPNN) with 3 encoder and 3 decoder layers
- **Input**: PDB structure files (backbone atoms only)
- **Parameters**: ~128-dimensional hidden representations
- **K-neighbors**: 32 nearest neighbors for graph construction

## Links

- **Original Repository**: [https://github.com/baker-laboratory/NA-MPNN](https://github.com/baker-laboratory/NA-MPNN)
- **Paper**: (Link to paper when available)

## Citation

If you use NA-MPNN in your research, please cite the appropriate paper (citation to be added).

## License

This project is licensed under the Apache 2.0 License.
