# Disaster Harvest

Disaster Harvest is a Django-based web application designed to manage and disseminate information about various disasters. It provides distinct dashboards for citizens and agencies, facilitating efficient communication and data management.

## Features

- **User Authentication**: Supports separate sign-up and login for citizens and agencies.
- **Disaster Management**: Agencies can add and manage disaster information.
- **Data Scraping**: Integrates functionality to scrape and update disaster data.
- **Custom Decorators**: Implements decorators like `agency_required` to restrict certain views to agency users.
- **Disast chatbot**: all Disaster based informations gathered here.

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/disaster_harvest.git
    cd disaster_harvest
    ```

2. **Create and activate a virtual environment**:

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    ```

3. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**:

    ```bash
    python manage.py migrate
    ```

5. **Create a superuser**:

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**:

    ```bash
    python manage.py runserver
    ```

7. **Access the application**:

    Open your browser and navigate to `http://127.0.0
