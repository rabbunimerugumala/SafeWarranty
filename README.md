# SafeWarranty
A python flask application used to Store digital copies of warranty cards for electronics, automobiles, and more.

venv in Python stands for "virtual environment." It's a tool that helps you create isolated environments for your Python projects. Here’s why it’s useful:

Dependency Management: Different projects can have different dependencies. With venv, you can manage these separately without conflicts.

Isolation: Keeps your global Python environment clean by isolating project-specific libraries.

Reproducibility: Makes it easy to share your project with others, ensuring they have the same environment setup.

Security: Reduces the risk of breaking other projects by installing or upgrading dependencies only within the virtual environment.

To create a virtual environment, you can use the following command:

python
python -m venv myenv
To activate the virtual environment:

On Windows:

bash
myenv\Scripts\activate
On macOS/Linux:

bash
source myenv/bin/activate
Once activated, you can install packages using pip, and they will be available only within that environment.
