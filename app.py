import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.sampling import BayesianModelSampling

class MedicalDiagnosisBayesianNetwork:
    def __init__(self):
        # Define the Bayesian Network
        self.model = BayesianNetwork([
            ('Smoking', 'LungCancer'),
            ('LungCancer', 'ShortnessOfBreath')
        ])

        # Conditional Probability Distributions
        cpd_smoking = TabularCPD(
            variable='Smoking', 
            variable_card=2, 
            values=[[0.7], [0.3]]  # 30% chance of smoking
        )

        cpd_lung_cancer = TabularCPD(
            variable='LungCancer', 
            variable_card=2, 
            values=[[0.99, 0.1],   # Not Cancer if Not Smoking
                    [0.01, 0.9]],  # Cancer if Smoking
            evidence=['Smoking'],
            evidence_card=[2]
        )

        cpd_shortness = TabularCPD(
            variable='ShortnessOfBreath', 
            variable_card=2, 
            values=[[0.9, 0.3],   # Not Shortness if No Cancer
                    [0.1, 0.7]],  # Shortness if Cancer
            evidence=['LungCancer'],
            evidence_card=[2]
        )

        # Add CPDs to the model
        self.model.add_cpds(cpd_smoking, cpd_lung_cancer, cpd_shortness)
        
        # Check model consistency
        assert self.model.check_model()

    def generate_samples(self, num_samples=10000):
        inference = BayesianModelSampling(self.model)
        samples = inference.forward_sample(size=num_samples)
        return samples

    def visualize_samples(self, samples):
        # Create a figure with multiple subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Smoking vs Lung Cancer
        smoking_cancer_counts = samples.groupby(['Smoking', 'LungCancer']).size().unstack(fill_value=0)
        smoking_cancer_counts.plot(kind='bar', stacked=True, ax=ax1)
        ax1.set_title('Smoking vs Lung Cancer')
        ax1.set_xlabel('Smoking Status')
        ax1.set_ylabel('Number of Samples')
        ax1.legend(title='Lung Cancer', labels=['No Cancer', 'Cancer'])
        
        # Lung Cancer vs Shortness of Breath
        cancer_breath_counts = samples.groupby(['LungCancer', 'ShortnessOfBreath']).size().unstack(fill_value=0)
        cancer_breath_counts.plot(kind='bar', stacked=True, ax=ax2)
        ax2.set_title('Lung Cancer vs Shortness of Breath')
        ax2.set_xlabel('Lung Cancer Status')
        ax2.set_ylabel('Number of Samples')
        ax2.legend(title='Shortness of Breath', labels=['No Breath Issue', 'Breath Issue'])
        
        plt.tight_layout()
        return fig

def main():
    # Streamlit App Configuration
    st.set_page_config(
        page_title="Medical Diagnosis Bayesian Network",
        page_icon="🩺",
        layout="wide"
    )

    # App Title
    st.title("🩺 Medical Diagnosis Bayesian Network Simulator")

    # Sidebar for User Inputs
    st.sidebar.header("Simulation Parameters")
    
    # Probability Sliders
    smoking_prob = st.sidebar.slider(
        "Smoking Probability (%)", 
        min_value=0, 
        max_value=100, 
        value=30
    )
    
    cancer_risk = st.sidebar.slider(
        "Lung Cancer Risk (%)", 
        min_value=0, 
        max_value=100, 
        value=10
    )
    
    breath_risk = st.sidebar.slider(
        "Shortness of Breath Risk (%)", 
        min_value=0, 
        max_value=100, 
        value=20
    )

    # Generate Samples Button
    if st.sidebar.button("Generate Samples"):
        # Create Bayesian Network Instance
        bn = MedicalDiagnosisBayesianNetwork()
        
        # Generate Samples
        samples = bn.generate_samples(num_samples=10000)
        
        # Visualization Section
        st.header("Sample Distribution Visualization")
        
        # Display Visualization
        fig = bn.visualize_samples(samples)
        st.pyplot(fig)
        
        # Sample Summary
        st.subheader("Sample Distribution Summary")
        summary = samples.groupby(['Smoking', 'LungCancer', 'ShortnessOfBreath']).size().reset_index(name='Count')
        st.dataframe(summary)

        # Probability Calculations
        st.subheader("Probability Insights")
        total_samples = len(samples)
        
        # Calculate Probabilities
        smokers = samples[samples['Smoking'] == 1]
        cancer_patients = samples[samples['LungCancer'] == 1]
        breath_issues = samples[samples['ShortnessOfBreath'] == 1]
        
        # Display Probability Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Smoking Rate", 
                f"{len(smokers) / total_samples * 100:.2f}%"
            )
        
        with col2:
            st.metric(
                "Lung Cancer Rate", 
                f"{len(cancer_patients) / total_samples * 100:.2f}%"
            )
        
        with col3:
            st.metric(
                "Shortness of Breath Rate", 
                f"{len(breath_issues) / total_samples * 100:.2f}%"
            )

if __name__ == "__main__":
    main()