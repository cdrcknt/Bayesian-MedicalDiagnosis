# Bayesian Medical Diagnosis

This project uses a Bayesian Network to simulate the relationship between smoking, lung cancer, and shortness of breath, providing insights into medical diagnosis.

## Project Features:
- Generates samples based on user input for smoking, lung cancer risk, and shortness of breath.
- Visualizes the relationships between smoking, lung cancer, and shortness of breath using bar plots.
- Displays probability insights, showing the rates of smoking, lung cancer, and shortness of breath in the generated samples.

## How to Use:
1. Adjust the sliders in the sidebar to set the probability values for smoking, lung cancer, and shortness of breath.
2. Click the "Generate Samples" button to generate the samples and visualize the results.
3. The app will show a bar chart visualization and sample distribution summary.

## Technologies Used:
- **Streamlit** for creating the interactive web app.
- **pgmpy** for creating and sampling the Bayesian Network.
- **Matplotlib** and **Seaborn** for data visualization.

## Deployment
To access the app, visit: [Bayesian Medical Diagnosis App](https://bayesian-medicaldiagnosis.streamlit.app/)

## Installation
To run this app locally:
1. Clone the repository:
    ```bash
    git clone https://github.com/cdrcknt/Bayesian-MedicalDiagnosis.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Bayesian-MedicalDiagnosis
    ```
3. Set up a virtual environment:
    ```bash
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```
5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
6. Run the app:
    ```bash
    streamlit run app.py
    ```

## Developers
Cedric Kent Centeno
