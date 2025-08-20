This project is the first module in my MES (Manufacturing Execution System) mini-project portfolio. It demonstrates how core MES features can be simulated using Python, Streamlit, and SQLite.

Project Overview:
The Production Order Tracking app allows you to:

Create and manage production orders

Assign operators to orders

Update order statuses (Scheduled → In Progress → Completed → On Hold/Cancelled)

Visualize real-time WIP (Work in Progress) with interactive charts

This is a simplified MES-like system that shows how manufacturing operations can be digitized at the shop-floor level.

Tech Stack

Python — backend logic

Streamlit — interactive UI

SQLite — database storage

Plotly — visualizations

Features Demo

Add new orders with product name and quantity

Assign operators to each order

Update the status as the order moves through the lifecycle

View WIP status in a real-time bar chart

How to Run Locally
# Clone the repo (or download as ZIP)
git clone https://github.com/SrineeshKonda89/MES-Mini-Portfolio.git
cd MES-Mini-Portfolio

# Create virtual environment
python -m venv venv
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py


The app will open in your browser at http://localhost:8501.

