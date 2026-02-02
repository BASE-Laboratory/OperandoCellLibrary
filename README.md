# Faraday/STFC Operando Sample Environment Library

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://operando-library.streamlit.app)
[![arXiv](https://img.shields.io/badge/arXiv-2601.00851-b31b1b.svg)](https://arxiv.org/abs/2601.00851)

**The open-access hardware registry for the UK battery community.**

This repository hosts the machine-readable registry of sample environments (electrochemical cells) available across UK central facilities (ISIS, Diamond Light Source, etc.). It serves as the hardware ground truth for the **Heuristic Operando** framework, enabling researchers and AI agents to match experimental requirements with compatible hardware specifications.

## Live Dashboard
Access the interactive tool here: **[Launch Registry](https://operando-library.streamlit.app)**

## 📖 Context
This registry supports the perspective article:

> **Autonomous battery research: Principles of heuristic operando experimentation** > *Emily Lu, Gabriel Perez, Peter Baker, Daniel Irving, Santosh Kumar, Veronica Celorrio, Sylvia Britto, Thomas F. Headen, Miguel Gomez-Gonzalez, Connor Wright, Calum Green, Robert Scott Young, Oleg Kirichek, Ali Mortazavi, Sarah Day, Isabel Antony, Zoe Wright, Thomas Wood, Tim Snow, Jeyan Thiyagalingam, Paul Quinn, Martin Owen Jones, William David, James Le Houx* > arXiv:2601.00851 (2026) · [Read the Preprint](https://arxiv.org/abs/2601.00851)

It addresses the 3Rs of experimental hardware:
* **Reliability:** Tracking failure modes (e.g., beam damage, vibrations).
* **Representativeness:** Quantifying trade-offs between TRL and signal quality.
* **Reproducibility:** Standardizing metadata for pressure control and assembly.

## Repository Structure
* `app.py`: The Streamlit dashboard source code.
* `operando_cell_registry.json`: The master database (JSON). This file adheres to the schema required for Digital Twin integration.
* `requirements.txt`: Python dependencies.

## Local Usage
To run this dashboard on your own machine:

1.  Clone the repository:
    ```bash
    git clone [https://github.com/Base-Laboratory/OperandoCellLibrary.git](https://github.com/Base-Laboratory/OperandoCellLibrary.git)
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the app:
    ```bash
    streamlit run app.py
    ```

## Contributing
This is an Open Science initiative. We welcome contributions from beamline scientists and researchers.
* **New Cells:** Please submit a Pull Request adding your cell's JSON entry to `operando_cell_registry.json`.
* **Corrections:** If you spot an error in specifications (e.g., Max Temp), please open an Issue.

## License
This project is licensed under the BSD 3 Clause License - see the LICENSE file for details.

## Contact
Maintained by **James Le Houx** (STFC / The Faraday Institution).
