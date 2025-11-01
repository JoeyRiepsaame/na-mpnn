# Hugging Face Space Deployment Guide

This guide provides step-by-step instructions for deploying NA-MPNN as a Hugging Face Space.

## Prerequisites

- A Hugging Face account (free at [huggingface.co](https://huggingface.co))
- Git installed on your local machine
- This NA-MPNN repository

## Step 1: Create a New Space

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. Fill in the Space details:
   - **Space name**: Choose a name (e.g., `na-mpnn`)
   - **License**: Apache 2.0 (or your preferred license)
   - **Space SDK**: Select **Gradio**
   - **Visibility**: Choose Public or Private

3. Click "Create Space"

## Step 2: Prepare Your Repository

From your local NA-MPNN repository:

```bash
# Navigate to your repository
cd /path/to/na-mpnn

# Rename README_HF.md to README.md for Hugging Face
# (You may want to backup the original README.md first)
mv README.md README_LOCAL.md
mv README_HF.md README.md

# Add Hugging Face as a remote
git remote add hf https://huggingface.co/spaces/<your-username>/<space-name>
```

Replace `<your-username>` and `<space-name>` with your actual Hugging Face username and Space name.

## Step 3: Push to Hugging Face

```bash
# Push the repository to Hugging Face
git push hf main
```

If you're working on a different branch:
```bash
git push hf <your-branch>:main
```

## Step 4: Wait for Deployment

Hugging Face will automatically:
1. Detect the Gradio SDK from the YAML frontmatter in README.md
2. Install dependencies from requirements.txt
3. Build and start the app.py

This process typically takes 2-5 minutes. You can monitor the build logs in the Space's "Logs" tab.

## Step 5: Access Your Space

Once deployed, your Space will be available at:
```
https://huggingface.co/spaces/<your-username>/<space-name>
```

## Troubleshooting

### Common Issues

**1. Build fails with dependency errors:**
- Check that all dependencies in `requirements.txt` are available on PyPI
- Ensure version numbers are compatible

**2. App doesn't start:**
- Check the logs tab for error messages
- Verify that `app.py` is in the root directory
- Ensure YAML frontmatter in README.md is correctly formatted

**3. Model files not found:**
- Ensure the `models/` directory is included in your push
- Verify paths in app.py match the repository structure

**4. Out of memory errors:**
- Hugging Face Spaces have limited resources
- Consider using smaller batch sizes
- Reduce the number of sequences generated per request

## Updating Your Space

To update your deployed Space:

```bash
# Make changes to your code
git add .
git commit -m "Update: description of changes"

# Push to Hugging Face
git push hf main
```

The Space will automatically rebuild and redeploy with your changes.

## Space Configuration

### Hardware Settings

Free Spaces run on CPU. For better performance:
1. Go to your Space settings
2. Select "Hardware" tab
3. Choose a GPU if available (may require subscription)

### Environment Variables

If you need to set environment variables:
1. Go to Space settings
2. Select "Variables and secrets" tab
3. Add your variables

## Local Testing

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Open http://localhost:7860 in your browser to test the interface.

## Best Practices

1. **Version Control**: Keep your original README.md backed up
2. **Testing**: Always test locally before pushing to Hugging Face
3. **Documentation**: Update README_HF.md with usage examples and citations
4. **Model Files**: Ensure model checkpoint files are committed (they're large ~27MB each)
5. **Examples**: Include example PDB files in the repository

## Resources

- [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces)
- [Gradio Documentation](https://gradio.app/docs/)
- [NA-MPNN Repository](https://github.com/baker-laboratory/NA-MPNN)

## Support

If you encounter issues:
1. Check the Space's "Logs" tab for error messages
2. Review the Hugging Face Spaces documentation
3. Open an issue in the NA-MPNN repository
