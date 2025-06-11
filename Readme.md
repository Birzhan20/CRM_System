
# CRM System

## Overview
This project is a Customer Relationship Management (CRM) system designed to automate client management processes, including lead tracking, service management, advertising campaigns, contract creation, and campaign performance analytics. The system supports role-based access for administrators, operators, marketers, and managers, ensuring secure and efficient workflows.

## Features
- **User Authentication and Roles**:
  - **Administrator**: Create, view, and edit users; assign roles and permissions.
  - **Operator**: Create, view, and edit potential clients.
  - **Marketer**: Manage services and advertising campaigns.
  - **Manager**: View potential clients, create/edit contracts, and convert potential clients to active clients.
  - All roles can view advertising campaign statistics.

- **Service Management**:
  - Create, edit, view, and delete services with fields for name, description, and cost.
  - List view with unique identifiers (e.g., service name) linking to detail pages.
  - Detail page with non-editable data, edit, and delete options.
  - Pre-filled edit page and empty create page.

- **Advertising Campaign Management**:
  - Create, edit, view, and delete campaigns with fields for name, promoted service, promotion channel, and budget.
  - Similar structure to service management (list, detail, edit, create pages).

- **Contract Management**:
  - Create, edit, view, and delete contracts with fields for name, service, document file, conclusion date, duration, and amount.
  - Similar structure to service management.

- **Client Management**:
  - Create, edit, view, and delete active clients, with pre-filled potential client data during creation.
  - List view with unique identifiers linking to detail pages, with edit and delete options.
  - Creation form includes potential client data and contract details.

- **Campaign Statistics**:
  - Tracks:
    - Number of potential clients attracted per campaign.
    - Number of clients converted from potential to active.
    - Revenue-to-advertising-cost ratio (based on contracts and campaign budgets).
  - Accessible to all user roles.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Birzhan20/CRM_System
   cd crm-system
   ```

2. **Set Up Environment**:
   - Ensure Python 3.12+ is installed.
   - Create and activate a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**:
   - Configure PostgreSQL and update the database URL in the configuration file (e.g., `.env`).
   - Run database migrations:
     ```bash
     alembic upgrade head
     ```

5. **Run the Application**:
   ```bash
   uvicorn app.main:app --reload
   ```
   - The API will be available at `http://localhost:8000`.

## Usage
- **API Access**:
  - Use tools like Postman or cURL to interact with the API endpoints.
  - Access the API documentation at `http://localhost:8000/docs` (Swagger UI) for detailed endpoint information.

- **Role-Based Workflow**:
  - **Admins**: Log in to create users and assign roles via `/users` endpoints.
  - **Operators**: Use `/potential-clients` endpoints to manage leads.
  - **Marketers**: Manage services (`/services`) and campaigns (`/campaigns`).
  - **Managers**: Access `/potential-clients`, `/contracts`, and `/active-clients` to manage contracts and client conversions.
  - All roles can view campaign statistics via `/campaigns/statistics`.

## Project Structure
```
crm-system/
├── backend/
│   ├── alembic          # Alembic migration files
│   ├── api/             # API route definitions   
│   ├── core/            # Database configuration 
│   ├── crud/            # CRUD Operations
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas for validation
│   ├── tests/           # Tests for API and CRUD
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py          # FastAPI application entry point
└── README.md            # Project documentation
```

## API Endpoints
### Auth
- `POST /token`: Authenticate user and return access token.
- `POST /refresh`: Refresh token.

### Services
- `GET /services`: List all services.
- `POST /services`: Create a new service.
- `GET /services/{id}`: View service details.
- `PUT /services/{id}`: Edit a service.
- `DELETE /services/{id}`: Delete a service.

### Advertising Campaigns
- `GET /ad_campaigns`: List all campaigns.
- `POST /ad_campaigns`: Create a new campaign.
- `GET /ad_campaigns/{ad_campaign_id}`: View campaign details.
- `PATCH /ad_campaigns/{ad_campaign_id}`: Edit a campaign.
- `DELETE /ad_campaigns/{ad_campaign_id}`: Delete a campaign.

### Clients
- `GET /clients`: List all potential clients.
- `POST /clients`: Create a new potential client.
- `GET /clients/{client_id}`: View client details.
- `PUT /clients/{client_id}`: Edit a potential client.
- `DELETE /clients/{client_id}`: Delete a potential client.


### Contracts
- `GET /contracts`: List all contracts.
- `POST /contracts`: Create a new contract.
- `GET /contracts/{contract_id}`: View contract details.
- `PUT /contracts/{contract_id}`: Edit a contract.
- `DELETE /contracts/{contract_id}`: Delete a contract.

### Users
- `GET /users`: List all users.
- `POST /users`: Create a new users.
- `GET /users/{user_id}`: View user details.
- `PATCH /users/{user_id}`: Edit an user.
- `DELETE /users/{user_id}`: Delete an user.

### Analytics
- `GET /statistics/campaigns`: Get all campaign stats
- `GET /statistics/campaigns/{campaign_id}`: Get campaign stats detail

## Database Schema
- **Users**: Stores user data.
- **Services**: Stores service details.
- **Ad_Campaigns**: Stores campaign details.
- **Contracts**: Stores contract data.
- **Clients**: Stores client data.

## Development Notes
- **Environment Variables**:
  - Set `DATABASE_URL` in `.env` for PostgreSQL connection.
  - Example: `DATABASE_URL=postgresql://user:password@localhost:5432/crm_db`

- **Testing**:
  - Run tests using:
    ```bash
    pytest
    ```

- **Migrations**:
  - Generate new migrations with:
    ```bash
    alembic revision --autogenerate -m "description"
    ```

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Create a pull request.

## License
This project is unlicensed.
