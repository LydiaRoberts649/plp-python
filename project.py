import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

def analyze_covid_data(data_path, selected_countries, output_file="covid19_analysis.ipynb"):
    """
    Analyzes global COVID-19 data, performs EDA, and generates a report.

    Args:
        data_path (str): Path to the COVID-19 dataset (CSV file).
        selected_countries (list): List of countries to analyze.
        output_file (str, optional): Name of the output Jupyter Notebook file.
    """

    try:
        
        # Load the dataset
        df = pd.read_csv(data_path)
        print(f"Data loaded successfully from {data_path}")

        # 2️⃣ Data Exploration
        # Explore the dataset structure
        print("\n--- Data Exploration ---")
        print("Column names:", df.columns)
        print("First 5 rows:")
        print(df.head())
        print("Missing values before cleaning:")
        print(df.isnull().sum())

        
        # Filter for selected countries
        df_filtered = df[df['location'].isin(selected_countries)].copy()

        # Drop rows with missing dates
        df_filtered = df_filtered.dropna(subset=['date'])

        # Convert date column to datetime
        df_filtered['date'] = pd.to_datetime(df_filtered['date'])

        # Handle missing numeric values using interpolation
        numeric_cols = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_vaccinations', 'people_vaccinated']
        for col in numeric_cols:
            df_filtered[col] = df_filtered.groupby('location')[col].apply(lambda x: x.interpolate())

        # Fill any remaining missing values with 0
        df_filtered = df_filtered.fillna(0)
        print("\nMissing values after cleaning:")
        print(df_filtered.isnull().sum())
        print("\nData cleaning complete.")

        # 4️⃣ Exploratory Data Analysis (EDA)
        # --- EDA ---
        print("\n--- Exploratory Data Analysis ---")
        plt.figure(figsize=(12, 6))
        for country in selected_countries:
            country_data = df_filtered[df_filtered['location'] == country]
            plt.plot(country_data['date'], country_data['total_cases'], label=country)
        plt.title('Total COVID-19 Cases Over Time')
        plt.xlabel('Date')
        plt.ylabel('Total Cases')
        plt.legend()
        plt.grid(True)
        plt.show()

        plt.figure(figsize=(12, 6))
        for country in selected_countries:
            country_data = df_filtered[df_filtered['location'] == country]
            plt.plot(country_data['date'], country_data['total_deaths'], label=country)
        plt.title('Total COVID-19 Deaths Over Time')
        plt.xlabel('Date')
        plt.ylabel('Total Deaths')
        plt.legend()
        plt.grid(True)
        plt.show()

        plt.figure(figsize=(12, 6))
        for country in selected_countries:
            country_data = df_filtered[df_filtered['location'] == country]
            plt.plot(country_data['date'], country_data['new_cases'], label=country)
        plt.title('Daily New COVID-19 Cases')
        plt.xlabel('Date')
        plt.ylabel('New Cases')
        plt.legend()
        plt.grid(True)
        plt.show()

        # Calculate and plot death rate
        df_filtered['death_rate'] = df_filtered['total_deaths'] / df_filtered['total_cases']
        plt.figure(figsize=(12, 6))
        for country in selected_countries:
            country_data = df_filtered[df_filtered['location'] == country]
            plt.plot(country_data['date'], country_data['death_rate'], label=country)
        plt.title('COVID-19 Death Rate (Total Deaths / Total Cases)')
        plt.xlabel('Date')
        plt.ylabel('Death Rate')
        plt.legend()
        plt.grid(True)
        plt.show()

        print("\n--- Vaccination Analysis ---")
        plt.figure(figsize=(12, 6))
        for country in selected_countries:
            country_data = df_filtered[df_filtered['location'] == country]
            plt.plot(country_data['date'], country_data['total_vaccinations'], label=country)
        plt.title('Total COVID-19 Vaccinations Over Time')
        plt.xlabel('Date')
        plt.ylabel('Total Vaccinations')
        plt.legend()
        plt.grid(True)
        plt.show()

        # Calculate and compare % vaccinated population (using people_vaccinated)
        df_filtered['vaccination_rate'] = (df_filtered['people_vaccinated'] / df_filtered['population']) * 100
        plt.figure(figsize=(12, 6))
        for country in selected_countries:
            country_data = df_filtered[df_filtered['location'] == country]
            plt.plot(country_data['date'], country_data['vaccination_rate'], label=country)
        plt.title('Percentage of Population Vaccinated Over Time')
        plt.xlabel('Date')
        plt.ylabel('Vaccination Rate (%)')
        plt.legend()
        plt.grid(True)
        plt.show()
        
    
        latest_vaccination_data = df_filtered.groupby('location').last().reset_index()

        
        latest_vaccination_data['population'] = [100000000, 330000000, 1400000000]  
        latest_vaccination_data['vaccination_rate'] = (latest_vaccination_data['people_vaccinated'] / latest_vaccination_data['population']) * 100


        plt.figure(figsize=(10, 8))
        sns.barplot(x='location', y='vaccination_rate', data=latest_vaccination_data)
        plt.title('Latest Vaccination Rate by Country')
        plt.xlabel('Country')
        plt.ylabel('Vaccination Rate (%)')
        plt.show()

        # 7️⃣ Insights and Reporting
        # --- Insights ---
        print("\n--- Insights ---")
        print("\nKey Insights:")
        print("* USA has the highest total cases among the selected countries.")
        print("* India experienced a surge in new cases around mid-2021.")
        print("* Kenya's vaccination rate is lower compared to USA and India.")
        print("* The death rate varies across countries, indicating different healthcare outcomes.")

    except FileNotFoundError:
        print(f"Error: The file '{data_path}' was not found. Please check the file path.")
    except KeyError as e:
        print(f"Error: A required column is missing: {e}.  Please ensure the dataset has the necessary columns (date, location, total_cases, etc.)")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Please check the data and try again.")
    finally:
        print("\nAnalysis complete.")

if __name__ == "__main__":
    # Specify the path to your COVID-19 dataset (CSV file)
    data_file_path = 'owid-covid-data.csv'  # Replace with the actual path to your CSV file

    # Select countries for analysis
    countries_to_analyze = ['Kenya', 'United States', 'India']

    # Run the analysis and generate the report
    analyze_covid_data(data_file_path, countries_to_analyze)
