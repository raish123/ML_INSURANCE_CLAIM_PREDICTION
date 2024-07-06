# Insurance Claim Prediction

## Project Overviews

This project aims to predict whether an insurance claim will be made based on various features of the policyholders. The dataset includes attributes such as age, sex, BMI, number of children, smoking status, region, charges, and whether an insurance claim was made.

## Dataset Features

- **age**: Age of the policyholder.
- **sex**: Gender of the policyholder (male, female).
- **bmi**: Body Mass Index, providing an indication of whether the policyholder is underweight, normal weight, overweight, or obese.
- **children**: Number of children/dependents covered by the insurance.
- **smoker**: Smoking status of the policyholder (yes, no).
- **region**: Residential area of the policyholder (e.g., northeast, southeast, southwest, northwest).
- **charges**: Annual medical charges billed to the insurance.
- **insuranceclaim**: Whether an insurance claim was made (0 for no, 1 for yes).

## Project Structure

- **data/**: Contains the dataset file(s).
- **notebooks/**: Jupyter notebooks for data exploration, preprocessing, and model training.
- **src/**: Source code for the project including data processing scripts and model implementation.
- **models/**: Saved models and their weights.
- **reports/**: Generated reports and analysis.
- **README.md**: Project overview and documentation.

## Installation

To run this project, you need to have Python installed along with the necessary libraries. You can install the required libraries using the following command:

```bash
pip install -r requirements.txt
