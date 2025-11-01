#!/usr/bin/env python
"""
Example script demonstrating how to use the NA-MPNN Gradio interface programmatically.

This can be useful for:
- Batch processing multiple PDB files
- Integration into automated workflows
- Testing and validation
"""

import sys
import os
from pathlib import Path

# Import the app functions
from app import run_design, run_specificity

class PDBFile:
    """Mock file object for passing PDB paths to the app functions"""
    def __init__(self, path):
        self.name = path

def example_design_mode():
    """Example: Run design mode on a PDB file"""
    print("=" * 60)
    print("Example 1: Design Mode")
    print("=" * 60)
    
    # Path to example PDB file
    pdb_path = "./inference/examples/4oqu.pdb"
    pdb_file = PDBFile(pdb_path)
    
    # Run design with custom parameters
    result = run_design(
        pdb_file=pdb_file,
        temperature=0.1,      # Lower = more conservative designs
        num_sequences=3,      # Generate 3 sequences
        seed=12345,          # For reproducibility
        design_na_only=False  # Design both protein and nucleic acids
    )
    
    print(f"\nDesign results for {pdb_path}:")
    print(result[:1000])  # Print first 1000 characters
    print("\n... (truncated)\n")

def example_design_na_only():
    """Example: Design only nucleic acids, keep protein fixed"""
    print("=" * 60)
    print("Example 2: Design Mode (NA only)")
    print("=" * 60)
    
    pdb_path = "./inference/examples/4oqu.pdb"
    pdb_file = PDBFile(pdb_path)
    
    result = run_design(
        pdb_file=pdb_file,
        temperature=0.2,      # Higher temperature for more diversity
        num_sequences=5,
        seed=42,
        design_na_only=True   # Only design nucleic acids
    )
    
    print(f"\nNA-only design results for {pdb_path}:")
    print(result[:1000])
    print("\n... (truncated)\n")

def example_specificity_mode():
    """Example: Predict DNA binding specificity"""
    print("=" * 60)
    print("Example 3: Specificity Mode")
    print("=" * 60)
    
    pdb_path = "./inference/examples/1am9.pdb"
    pdb_file = PDBFile(pdb_path)
    
    result = run_specificity(
        pdb_file=pdb_file,
        design_na_only=True  # Predict for NA positions only
    )
    
    print(f"\nSpecificity predictions for {pdb_path}:")
    print(result)
    print()

def batch_process_pdbs(pdb_dir, output_dir):
    """
    Example: Batch process multiple PDB files
    
    Args:
        pdb_dir: Directory containing PDB files
        output_dir: Directory to save results
    """
    print("=" * 60)
    print("Example 4: Batch Processing")
    print("=" * 60)
    
    pdb_dir = Path(pdb_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Find all PDB files
    pdb_files = list(pdb_dir.glob("*.pdb"))
    print(f"\nFound {len(pdb_files)} PDB files in {pdb_dir}\n")
    
    for pdb_path in pdb_files:
        print(f"Processing {pdb_path.name}...")
        
        pdb_file = PDBFile(str(pdb_path))
        
        # Run design
        result = run_design(
            pdb_file=pdb_file,
            temperature=0.1,
            num_sequences=2,
            seed=42,
            design_na_only=False
        )
        
        # Save results
        output_file = output_dir / f"{pdb_path.stem}_design.txt"
        with open(output_file, 'w') as f:
            f.write(result)
        
        print(f"  Saved to {output_file}")
    
    print(f"\nBatch processing complete. Results saved to {output_dir}\n")

def parse_design_output(output_text):
    """
    Example: Parse the design output to extract sequences
    
    Returns:
        List of tuples: (header, sequence)
    """
    print("=" * 60)
    print("Example 5: Parsing Design Output")
    print("=" * 60)
    
    lines = output_text.strip().split('\n')
    sequences = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('>'):
            header = line[1:]  # Remove '>'
            if i + 1 < len(lines) and not lines[i + 1].startswith('>'):
                sequence = lines[i + 1]
                sequences.append((header, sequence))
                i += 2
            else:
                i += 1
        else:
            i += 1
    
    print(f"\nExtracted {len(sequences)} sequences:")
    for i, (header, seq) in enumerate(sequences[:3], 1):
        print(f"\n{i}. {header}")
        print(f"   {seq[:60]}..." if len(seq) > 60 else f"   {seq}")
    
    return sequences

def main():
    """Run all examples"""
    # Change to repository directory
    os.chdir(Path(__file__).parent)
    
    print("\n" + "=" * 60)
    print("NA-MPNN Gradio Interface - Usage Examples")
    print("=" * 60 + "\n")
    
    # Example 1: Basic design
    example_design_mode()
    
    # Example 2: Design NA only
    example_design_na_only()
    
    # Example 3: Specificity prediction
    example_specificity_mode()
    
    # Example 4: Batch processing
    batch_process_pdbs(
        pdb_dir="./inference/examples",
        output_dir="/tmp/na_mpnn_batch_output"
    )
    
    # Example 5: Parse design output
    pdb_file = PDBFile("./inference/examples/4oqu.pdb")
    result = run_design(pdb_file, 0.1, 2, 42, False)
    parse_design_output(result)
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
