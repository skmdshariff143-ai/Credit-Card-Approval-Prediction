import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from configs.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)

class VizPlotter:
    """
    Handles plotting of distribution, correlation, and classification evaluation charts.
    """
    def __init__(self):
        paths = config.get_paths()
        self.reports_dir = paths["reports_dir"]
        os.makedirs(self.reports_dir, exist_ok=True)
        
    def plot_distribution(self, df: pd.DataFrame, column: str, filename: str):
        """
        Plots the histogram distribution of a specific feature.
        """
        logger.info(f"Plotting distribution of '{column}'...")
        try:
            plt.figure(figsize=(8, 5))
            sns.histplot(df[column], kde=True, bins=30, color='skyblue')
            plt.title(f"Distribution of {column}")
            plt.xlabel(column)
            plt.ylabel("Frequency")
            plt.tight_layout()
            
            output_path = os.path.join(self.reports_dir, filename)
            plt.savefig(output_path, dpi=300)
            plt.close()
            logger.info(f"Saved distribution plot to: {output_path}")
        except Exception as e:
            logger.error(f"Failed to plot distribution for {column}: {str(e)}")

    def plot_correlation_matrix(self, df: pd.DataFrame, filename: str):
        """
        Plots a correlation heatmap for numerical variables.
        """
        logger.info("Plotting correlation matrix heatmap...")
        try:
            # Select numerical types
            num_df = df.select_dtypes(include=['number'])
            
            plt.figure(figsize=(12, 10))
            sns.heatmap(num_df.corr(), annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
            plt.title("Correlation Matrix Heatmap")
            plt.tight_layout()
            
            output_path = os.path.join(self.reports_dir, filename)
            plt.savefig(output_path, dpi=300)
            plt.close()
            logger.info(f"Saved correlation heatmap to: {output_path}")
        except Exception as e:
            logger.error(f"Failed to plot correlation matrix: {str(e)}")
            
    def plot_target_balance(self, y: pd.Series, filename: str):
        """
        Plots a bar chart showing the balance of target classes.
        """
        logger.info("Plotting target balance countplot...")
        try:
            plt.figure(figsize=(6, 5))
            sns.countplot(x=y, palette="Set2")
            plt.title("Target Class Distribution")
            plt.xlabel("Approval Class Target (0=Good, 1=Bad)")
            plt.ylabel("Count")
            plt.tight_layout()
            
            output_path = os.path.join(self.reports_dir, filename)
            plt.savefig(output_path, dpi=300)
            plt.close()
            logger.info(f"Saved target balance plot to: {output_path}")
        except Exception as e:
            logger.error(f"Failed to plot target balance: {str(e)}")
