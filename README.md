# IP Management System  

This repository contains an IP Management System designed to efficiently organize and manage IP addresses. The system supports two types of user roles: administrators and regular users, each with tailored functionalities.

## General Features  

### Login and Logout Functionality  
The system ensures secure login and logout processes, validated through the school database and robust authentication mechanisms. Access is restricted to current school faculty, staff, and students. User permissions are role-specific, ensuring appropriate access control.


### Search and Filter  
Users can search and filter IP addresses based on various criteria such as IP address, device name, and user name. This functionality enables quick identification of specific IP addresses and devices. 


### Pop-up Notifications  
The system includes real-time pop-up notifications to inform users about important events, such as successful IP address assignments, requests, or system updates. This feature enhances user experience by providing instant feedback and alerts.

### Interactive Dashboard  
The interactive dashboard leverages mouse hover and click events, allowing users to view detailed information such as IP address allocation, device types, and user information. This feature provides an intuitive understanding of IP address distribution and system data. 

## Administrator Features  

### IP Address Calculation  
Administrators can calculate IP addresses based on subnet masks, determining the number of available IP addresses within a subnet and allocating them efficiently. Occupied IP addresses are identified, and the system displays the number of available IP addresses to facilitate effective management.  


### Assign IP Addresses  
Administrators can assign IP addresses to multiple users simultaneously. Allocation can be based on IP address ranges, user roles, and departments.

### Staff Query and Assignment  
Administrators can search for staff members and assign IP addresses accordingly. This feature ensures quick and accurate IP address allocation based on roles and departmental needs.  


### Tracking and Management  
The system tracks and manages all allocated IP addresses and their associated devices. Records include MAC addresses, user names, comments, and device types, ensuring comprehensive management.  


### IP Address Pool Management  
Administrators can manage a pool of available IP addresses, enabling efficient organization and allocation of IP address ranges.  


## User Features  

### IP Address Request  
Users can submit requests for IP address assignments. This feature ensures that users can request IP addresses based on their specific needs.  


### CSV Import and Export  
Users can import and export data using CSV files for detailed IP address management. This functionality supports streamlined data handling for administrators.  

## System Architecture  

### Flask Blueprints  
The application is modularized using Flask blueprints, facilitating organized development and maintenance of different components.  


### SOAP API Integration  
SOAP APIs are integrated to retrieve and update data from external sources. This enables seamless communication with external databases and services for data retrieval and updates.  

### MySQL Database  
The system uses MySQL for scalability and future expansion. The database is managed via SQLAlchemy ORM for efficient operations.  


### Apache and mod_wsgi Deployment  
The application is deployed using Apache and mod_wsgi, ensuring stability and security.  

### Docker Volumes
The Flask application (Apache/mod_wsgi) and the MySQL database are containerized separately using Docker Compose.

### Low Coupling Design  
A low-coupling design approach enhances code readability and maintainability, making the system easier to extend and debug.

### Unit Testing  
The system employs `pytest` for unit testing, utilizing a dedicated test database to prevent interference with the primary database.  


### Technologies Used  

- Python Flask  
- SOAP API  
- SQLAlchemy - MySQL  
- JavaScript  
- HTML/CSS  
- Apache - mod_wsgi
- Docker 
