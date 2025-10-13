#!/usr/bin/env python3
"""
CSV Data Processor

A practical script that demonstrates data processing capabilities.
This script can clean, analyze, and generate reports from CSV files.
"""

import sys
import os
from pathlib import Path

# Add the root directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from python_helpers.data_processing import (
    csv_to_dict,
    dict_to_csv,
    clean_data,
    group_by,
    filter_data,
    get_unique_values,
    calculate_stats,
    count_occurrences
)
from python_helpers.file_ops import ensure_directory


def create_sample_csv():
    """Create a sample CSV file for demonstration."""
    sample_data = [
        {"name": "John Doe", "age": "25", "department": "Engineering", "salary": "75000", "city": "New York"},
        {"name": "Jane Smith", "age": "30", "department": "Marketing", "salary": "65000", "city": "San Francisco"},
        {"name": "Bob Johnson", "age": "", "department": "Engineering", "salary": "80000", "city": "Seattle"},
        {"name": " Alice Brown ", "age": "28", "department": "HR", "salary": "60000", "city": "New York"},
        {"name": "Charlie Wilson", "age": "35", "department": "Engineering", "salary": "90000", "city": "Austin"},
        {"name": "Diana Davis", "age": "27", "department": "Marketing", "salary": "", "city": "San Francisco"},
        {"name": "Eve Martinez", "age": "32", "department": "HR", "salary": "62000", "city": "Chicago"},
    ]
    
    # Ensure output directory exists
    output_dir = ensure_directory("data_output")
    csv_file = output_dir / "employees.csv"
    
    if dict_to_csv(sample_data, csv_file):
        print(f"Sample CSV created: {csv_file}")
        return csv_file
    return None


def analyze_csv_data(csv_file):
    """Analyze the CSV data and generate insights."""
    print(f"\n=== Analyzing {csv_file.name} ===")
    
    # 1. Load data
    print("\n1. Loading data...")
    data = csv_to_dict(str(csv_file))
    if not data:
        print("Failed to load data!")
        return
    
    print(f"Loaded {len(data)} records")
    
    # 2. Clean data
    print("\n2. Cleaning data...")
    original_count = len(data)
    clean_records = clean_data(data, remove_empty=True, strip_strings=True)
    print(f"After cleaning: {len(clean_records)} records ({original_count - len(clean_records)} removed)")
    
    # 3. Basic statistics
    print("\n3. Basic Analysis:")
    print(f"   Total employees: {len(clean_records)}")
    
    # Get unique values for key fields
    departments = get_unique_values(clean_records, "department")
    cities = get_unique_values(clean_records, "city")
    
    print(f"   Departments: {len(departments)} ({', '.join(departments)})")
    print(f"   Cities: {len(cities)} ({', '.join(cities)})")
    
    # 4. Department distribution
    print("\n4. Department Distribution:")
    dept_counts = count_occurrences(clean_records, "department")
    for dept, count in dept_counts.items():
        print(f"   {dept}: {count} employees")
    
    # 5. City distribution
    print("\n5. City Distribution:")
    city_counts = count_occurrences(clean_records, "city")
    for city, count in city_counts.items():
        print(f"   {city}: {count} employees")
    
    # 6. Salary analysis (for records with salary data)
    print("\n6. Salary Analysis:")
    salary_data = [int(record['salary']) for record in clean_records 
                   if record.get('salary') and record['salary'].isdigit()]
    
    if salary_data:
        salary_stats = calculate_stats(salary_data)
        print(f"   Records with salary data: {salary_stats['count']}")
        print(f"   Average salary: ${salary_stats['mean']:,.2f}")
        print(f"   Median salary: ${salary_stats['median']:,.2f}")
        print(f"   Salary range: ${salary_stats['min']:,.2f} - ${salary_stats['max']:,.2f}")
        print(f"   Standard deviation: ${salary_stats['std_dev']:,.2f}")
    
    # 7. Group analysis
    print("\n7. Analysis by Department:")
    dept_groups = group_by(clean_records, "department")
    
    for dept, employees in dept_groups.items():
        print(f"\n   {dept} Department ({len(employees)} employees):")
        
        # Average age in department
        ages = [int(emp['age']) for emp in employees 
                if emp.get('age') and emp['age'].isdigit()]
        if ages:
            avg_age = sum(ages) / len(ages)
            print(f"     Average age: {avg_age:.1f} years")
        
        # Average salary in department
        dept_salaries = [int(emp['salary']) for emp in employees 
                        if emp.get('salary') and emp['salary'].isdigit()]
        if dept_salaries:
            avg_salary = sum(dept_salaries) / len(dept_salaries)
            print(f"     Average salary: ${avg_salary:,.2f}")
        
        # Cities represented
        dept_cities = get_unique_values(employees, "city")
        print(f"     Cities: {', '.join(dept_cities)}")
    
    # 8. Generate filtered reports
    print("\n8. Generating filtered reports...")
    
    # High earners (>= $70k)
    high_earners = [emp for emp in clean_records 
                   if emp.get('salary') and emp['salary'].isdigit() 
                   and int(emp['salary']) >= 70000]
    
    output_dir = csv_file.parent
    
    if high_earners:
        high_earners_file = output_dir / "high_earners_report.csv"
        if dict_to_csv(high_earners, high_earners_file):
            print(f"   High earners report: {high_earners_file} ({len(high_earners)} employees)")
    
    # Engineering department
    engineering_filter = filter_data(clean_records, {"department": "Engineering"})
    if engineering_filter:
        eng_file = output_dir / "engineering_employees.csv"
        if dict_to_csv(engineering_filter, eng_file):
            print(f"   Engineering report: {eng_file} ({len(engineering_filter)} employees)")
    
    return clean_records


def main():
    """Main function to run the CSV processor."""
    print("=== CSV Data Processor ===")
    print("This script demonstrates data processing capabilities of Python Helpers")
    
    # Create sample data
    csv_file = create_sample_csv()
    if not csv_file:
        print("Failed to create sample CSV!")
        return
    
    # Analyze the data
    analyze_csv_data(csv_file)
    
    print(f"\n=== Analysis Complete ===")
    print(f"Check the 'data_output' directory for generated reports.")


if __name__ == "__main__":
    main()