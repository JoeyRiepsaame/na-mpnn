# Hugging Face Space Setup - Complete Summary

## Overview

This document provides a complete summary of the Hugging Face Space setup for NA-MPNN, including all changes made, testing results, and deployment instructions.

## Changes Made

### New Files Created

1. **app.py** (Main Gradio Application)
   - Provides web interface with two modes:
     - **Design Mode**: Generate protein and nucleic acid sequences for backbone structures
     - **Specificity Mode**: Predict DNA binding specificity (PPM)
   - Secure implementation with input validation
   - Uses subprocess to call existing inference code
   - Handles file uploads and provides formatted outputs
   - Includes comprehensive error handling

2. **requirements.txt** (Python Dependencies)
   ```
   numpy==2.0.2
   pandas==2.2.3
   prody==2.4.1
   torch==2.5.1
   gradio==5.5.0
   ```

3. **README_HF.md** (Hugging Face Space Documentation)
   - Contains YAML frontmatter for HF Space configuration
   - Provides user-friendly documentation
   - Includes usage instructions and examples
   - Explains sequence encoding scheme

4. **.gitignore** (Version Control)
   - Excludes Python cache files
   - Excludes temporary directories
   - Excludes build artifacts
   - Excludes Gradio cache

5. **HUGGINGFACE_DEPLOYMENT.md** (Deployment Guide)
   - Step-by-step deployment instructions
   - Troubleshooting section
   - Best practices
   - Configuration options

6. **examples_gradio_usage.py** (Usage Examples)
   - Programmatic usage examples
   - Batch processing example
   - Output parsing examples
   - Integration examples

### Modified Files

1. **README.md**
   - Added Hugging Face Space section at the beginning
   - Added deployment instructions section at the end
   - Includes links and usage examples
   - Maintains all original content

## Security Measures

All security vulnerabilities have been addressed:

✅ **Input Validation**
- PDB file paths are validated using `os.path.abspath()` and `os.path.isfile()`
- Numeric inputs are type-checked and converted
- File existence is verified before processing

✅ **Subprocess Security**
- All subprocess calls use `shell=False` explicitly
- Commands are passed as lists, not strings
- No shell interpretation of user input

✅ **CodeQL Scan Results**
- Initial scan: 1 alert (command injection)
- After fixes: 0 alerts
- All security issues resolved

## Testing Results

### Design Mode Testing
```
Test Case: 4oqu.pdb
Parameters: temperature=0.1, num_sequences=2, seed=42
Result: ✅ PASS
- Successfully generated 2 sequences
- Output includes confidence scores
- Sequence encoding is correct
```

### Specificity Mode Testing
```
Test Case: 1am9.pdb
Parameters: design_na_only=True
Result: ✅ PASS
- Successfully generated PPM for 43 DNA positions
- Output format is correct
- Probability values sum to ~1.0 per position
```

### Batch Processing Testing
```
Test Case: Multiple PDB files in examples/
Result: ✅ PASS
- Processed all PDB files successfully
- Outputs saved correctly
- No errors during batch processing
```

### Security Testing
```
Test Case: Input validation
Result: ✅ PASS
- Invalid file paths rejected
- Non-numeric inputs handled
- CodeQL scan passes with 0 alerts
```

## Deployment Instructions

### Quick Start

1. **Create Hugging Face Space**
   - Go to https://huggingface.co/new-space
   - Select Gradio SDK
   - Choose your Space name

2. **Prepare Repository**
   ```bash
   # Rename README_HF.md to README.md for HF
   mv README.md README_LOCAL.md
   mv README_HF.md README.md
   
   # Add HF remote
   git remote add hf https://huggingface.co/spaces/<username>/<space-name>
   ```

3. **Deploy**
   ```bash
   git push hf main
   ```

4. **Access**
   - Space will be available at: `https://huggingface.co/spaces/<username>/<space-name>`
   - Build typically takes 2-5 minutes

### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Access at http://localhost:7860
```

## Features

### Design Mode Features
- Upload PDB file with protein-nucleic acid complex
- Adjustable sampling temperature (0.05 - 1.0)
- Generate 1-10 sequences per run
- Random seed for reproducibility
- Option to design only nucleic acids (keep protein fixed)
- Formatted output with confidence scores
- Sequence legend included

### Specificity Mode Features
- Upload PDB file with protein-DNA complex
- Predict position probability matrix (PPM)
- DNA binding specificity predictions
- Formatted table output
- Position-by-position analysis

### User Interface
- Clean, intuitive tabbed interface
- File upload with drag-and-drop support
- Real-time parameter adjustment
- Clear error messages
- Comprehensive documentation

## File Structure

```
na-mpnn/
├── app.py                          # Main Gradio application
├── requirements.txt                # Python dependencies
├── README.md                       # Original repository README
├── README_HF.md                    # Hugging Face Space README
├── .gitignore                      # Git ignore rules
├── HUGGINGFACE_DEPLOYMENT.md       # Deployment guide
├── HUGGINGFACE_SPACE_SETUP.md     # This file
├── examples_gradio_usage.py       # Usage examples
├── inference/
│   ├── run.py                     # Inference script
│   ├── data_utils.py              # Data utilities
│   ├── model_utils.py             # Model utilities
│   └── examples/
│       ├── 4oqu.pdb               # Example for design
│       └── 1am9.pdb               # Example for specificity
├── models/
│   ├── design_model/
│   │   └── s_19137.pt             # Design model weights (~27MB)
│   └── specificity_model/
│       └── s_70114.pt             # Specificity model weights (~27MB)
└── [other repository files]
```

## Performance Considerations

### Resource Requirements
- **CPU**: Works on CPU, GPU recommended for faster inference
- **Memory**: ~2GB RAM minimum
- **Storage**: ~100MB for dependencies + ~54MB for model weights
- **Processing Time**: 
  - Design mode: ~30-60 seconds for 2-3 sequences
  - Specificity mode: ~60-90 seconds for PPM prediction

### Optimization Tips
1. Use smaller batch sizes for faster response
2. Enable GPU if available in HF Space settings
3. Consider timeout settings for large structures
4. Cache model loading for repeated requests

## Troubleshooting

### Common Issues

**Issue**: Build fails with dependency errors
- **Solution**: Check requirements.txt versions match available packages

**Issue**: Model files not found
- **Solution**: Ensure models/ directory is included in git push

**Issue**: Timeout errors
- **Solution**: Increase timeout in subprocess.run() calls or use smaller batch sizes

**Issue**: Out of memory
- **Solution**: Reduce batch size or number of sequences generated

## Documentation

Complete documentation is available in:
1. **README_HF.md** - User-facing documentation for HF Space
2. **README.md** - Developer documentation (original)
3. **HUGGINGFACE_DEPLOYMENT.md** - Deployment guide
4. **examples_gradio_usage.py** - Code examples

## Support

For issues or questions:
1. Check the deployment guide: HUGGINGFACE_DEPLOYMENT.md
2. Review usage examples: examples_gradio_usage.py
3. Open an issue in the repository
4. Consult Hugging Face Spaces documentation

## Version Information

- **NA-MPNN**: Latest version from repository
- **Gradio**: 5.5.0
- **PyTorch**: 2.5.1
- **Python**: 3.12+ recommended

## License

This setup follows the same license as the NA-MPNN repository (Apache 2.0).

## Credits

- **NA-MPNN**: Original model and inference code
- **Gradio**: Web interface framework
- **Hugging Face**: Hosting platform

## Future Enhancements

Potential improvements for future versions:
- Add example PDB files directly in the interface
- Include visualization of structures
- Add batch processing UI
- Export results in multiple formats
- Add model performance metrics display
- Include structure validation

---

**Setup Complete**: The repository is ready for deployment to Hugging Face Spaces! 🚀
