# Contributing to setup_coral

Thank you for your interest in contributing to this Coral USB Accelerator setup repository!

## How to Contribute

### Reporting Issues

If you encounter any problems with the setup scripts or documentation:

1. Check if the issue already exists in the [Issues](https://github.com/BaoBao112233/setup_coral/issues) section
2. If not, create a new issue with:
   - Clear description of the problem
   - Your operating system and version
   - Python version
   - Steps to reproduce
   - Error messages or logs

### Suggesting Enhancements

We welcome suggestions for improvements:

1. Open an issue with the "enhancement" tag
2. Describe the enhancement clearly
3. Explain why it would be useful
4. Provide examples if applicable

### Contributing Code

#### Setting Up Development Environment

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/setup_coral.git
   cd setup_coral
   ```

3. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Code Standards

**Python Code:**
- Follow PEP 8 style guide
- Use Python 3.7+ compatible syntax
- Include docstrings for functions and classes
- Handle errors gracefully with informative messages
- Test your code before submitting

**Shell Scripts:**
- Use bash for compatibility
- Include comments for complex operations
- Use `set -e` to exit on errors
- Provide colored output for user feedback
- Test on multiple Linux distributions if possible

**Documentation:**
- Use clear, concise language
- Include code examples where appropriate
- Keep formatting consistent with existing docs
- Test all commands and examples

#### Testing Your Changes

1. Test Python scripts:
   ```bash
   python3 -m py_compile *.py
   python3 test_coral.py
   ```

2. Test shell scripts:
   ```bash
   bash -n setup_coral.sh
   bash -n download_models.sh
   ```

3. Test actual functionality if you have a Coral device

#### Submitting Changes

1. Commit your changes with clear messages:
   ```bash
   git add .
   git commit -m "Add feature: description of what you did"
   ```

2. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a Pull Request:
   - Provide a clear title and description
   - Reference any related issues
   - Explain what changes you made and why
   - Include test results if applicable

### Areas for Contribution

We especially welcome contributions in these areas:

1. **Platform Support:**
   - Improve Windows installation instructions
   - Add macOS-specific scripts
   - Test and document on different Linux distributions

2. **Examples:**
   - Add more example scripts (object detection, pose estimation, etc.)
   - Create Jupyter notebooks
   - Add real-world use case examples

3. **Testing:**
   - Automated testing scripts
   - CI/CD pipeline improvements
   - Cross-platform testing

4. **Documentation:**
   - Translations to other languages
   - Video tutorials
   - Troubleshooting guides for specific issues

5. **Performance:**
   - Optimization tips
   - Benchmark comparisons
   - Performance tuning guides

## Code Review Process

1. All submissions require review
2. Maintainers will review your PR
3. Address any feedback or requested changes
4. Once approved, your PR will be merged

## Community Guidelines

- Be respectful and inclusive
- Help others when you can
- Provide constructive feedback
- Follow the code of conduct

## Questions?

If you have questions about contributing:
- Open an issue with the "question" tag
- Check existing issues and discussions
- Review the README and documentation first

## License

By contributing, you agree that your contributions will be licensed under the same terms as the project.

## Acknowledgments

Contributors will be acknowledged in the project. Thank you for helping improve this resource!
