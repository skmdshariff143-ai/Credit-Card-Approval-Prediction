import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from configs.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class VizPlotter:
    """
    Enterprise-grade plotting utility for generating and saving Univariate,
    Bivariate, Multivariate, and Outlier detection charts during EDA.
    """

    def __init__(self):
        paths = config.get_paths()
        # Direct folder screenshots/eda/ as required
        self.eda_screenshots_dir = os.path.join(paths["raw_dir"].parent.parent, "screenshots", "eda")
        os.makedirs(self.eda_screenshots_dir, exist_ok=True)

    def plot_distribution(self, df: pd.DataFrame, column: str, filename: str):
        """
        Generates and saves a histogram distribution with KDE overlay for a numeric column.
        """
        logger.info(f"Generating distribution plot for '{column}'...")
        try:
            plt.figure(figsize=(8, 5))
            sns.histplot(df[column], kde=True, bins=30, color="skyblue")
            plt.title(f"Distribution of {column}", fontsize=14, fontweight="bold")
            plt.xlabel(column)
            plt.ylabel("Frequency")
            plt.tight_layout()

            output_path = os.path.join(self.eda_screenshots_dir, filename)
            plt.savefig(output_path, dpi=300)
            plt.close()
            logger.info(f"Saved distribution plot to: {output_path}")
        except Exception as e:
            logger.error(f"Failed to plot distribution for {column}: {str(e)}")

    def plot_target_balance(self, y: pd.Series, filename: str):
        """
        Generates a count plot for the target binary classes.
        """
        logger.info("Generating target balance count plot...")
        try:
            plt.figure(figsize=(6, 5))
            sns.countplot(x=y, palette="Set2")
            plt.title("Target Class Distribution (STATUS_TARGET)", fontsize=14, fontweight="bold")
            plt.xlabel("Approval Class Target (0 = Approved, 1 = Rejected)")
            plt.ylabel("Count")
            plt.tight_layout()

            output_path = os.path.join(self.eda_screenshots_dir, filename)
            plt.savefig(output_path, dpi=300)
            plt.close()
            logger.info(f"Saved target balance plot to: {output_path}")
        except Exception as e:
            logger.error(f"Failed to plot target balance: {str(e)}")

    def plot_correlation_heatmap(self, df: pd.DataFrame, filename: str):
        """
        Plots a correlation heatmap for all numerical features.
        """
        logger.info("Generating correlation matrix heatmap...")
        try:
            num_df = df.select_dtypes(include=["number"])
            plt.figure(figsize=(10, 8))
            sns.heatmap(num_df.corr(), annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
            plt.title("Numerical Features Correlation Matrix", fontsize=14, fontweight="bold")
            plt.tight_layout()

            output_path = os.path.join(self.eda_screenshots_dir, filename)
            plt.savefig(output_path, dpi=300)
            plt.close()
            logger.info(f"Saved correlation heatmap to: {output_path}")
        except Exception as e:
            logger.error(f"Failed to plot correlation heatmap: {str(e)}")

    def plot_categorical_vs_target(self, df: pd.DataFrame, col: str, target_col: str, filename: str):
        """
        Plots categorical relationship vs target using a grouped countplot.
        """
        logger.info(f"Generating count plot for '{col}' vs target '{target_col}'...")
        try:
            plt.figure(figsize=(10, 6))
            sns.countplot(data=df, x=col, hue=target_col, palette="viridis")
            plt.title(f"{col} vs Approval Status", fontsize=14, fontweight="bold")
            plt.xticks(rotation=45, ha="right")
            plt.xlabel(col)
            plt.ylabel("Count")
            plt.legend(title=target_col, labels=["Approved (0)", "Rejected (1)"])
            plt.tight_layout()

            output_path = os.path.join(self.eda_screenshots_dir, filename)
            plt.savefig(output_path, dpi=300)
            plt.close()
            logger.info(f"Saved bivariate categorical plot to: {output_path}")
        except Exception as e:
            logger.error(f"Failed to plot categorical vs target for {col}: {str(e)}")

    def plot_numeric_vs_target_box(self, df: pd.DataFrame, num_col: str, target_col: str, filename: str):
        """
        Plots a boxplot of a numeric feature vs target.
        """
        logger.info(f"Generating boxplot of '{num_col}' vs target '{target_col}'...")
        try:
            plt.figure(figsize=(7, 5))
            sns.boxplot(data=df, x=target_col, y=num_col, palette="Set1")
            plt.title(f"{num_col} Distribution by Approval Status", fontsize=14, fontweight="bold")
            plt.xlabel("Approval Status (0 = Approved, 1 = Rejected)")
            plt.ylabel(num_col)
            plt.tight_layout()

            output_path = os.path.join(self.eda_screenshots_dir, filename)
            plt.savefig(output_path, dpi=300)
            plt.close()
            logger.info(f"Saved bivariate boxplot to: {output_path}")
        except Exception as e:
            logger.error(f"Failed to plot numeric vs target for {num_col}: {str(e)}")

    def plot_outliers_boxplot(self, df: pd.DataFrame, num_col: str, filename: str):
        """
        Plots a univariate boxplot for outlier inspection.
        """
        logger.info(f"Generating outlier boxplot for '{num_col}'...")
        try:
            plt.figure(figsize=(6, 4))
            sns.boxplot(y=df[num_col], color="lightcoral")
            plt.title(f"Outlier Boxplot - {num_col}", fontsize=14, fontweight="bold")
            plt.ylabel(num_col)
            plt.tight_layout()

            output_path = os.path.join(self.eda_screenshots_dir, filename)
            plt.savefig(output_path, dpi=300)
            plt.close()
            logger.info(f"Saved outlier boxplot to: {output_path}")
        except Exception as e:
            logger.error(f"Failed to plot outliers boxplot for {num_col}: {str(e)}")
