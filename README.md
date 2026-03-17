# IP Management System  

This repository contains an IP Management System designed to efficiently organize and manage IP addresses. The system supports two types of user roles: administrators and regular users, each with tailored functionalities.

## General Features  

### Login and Logout Functionality  
The system ensures secure login and logout processes, validated through the school database and robust authentication mechanisms. Access is restricted to current school faculty, staff, and students. User permissions are role-specific, ensuring appropriate access control.

<img width="300" height="200" alt="1" src="https://github.com/user-attachments/assets/e595a067-0755-4eca-b0dd-d8e20c9e031b" />

### Search and Filter  
Users can search and filter IP addresses based on various criteria such as IP address, device name, and user name. This functionality enables quick identification of specific IP addresses and devices. 

<img width="500" height="100" alt="2" src="https://github.com/user-attachments/assets/aa2646dd-e160-47e5-9f63-d16df0098dcf" />

### Pop-up Notifications  
The system includes real-time pop-up notifications to inform users about important events, such as successful IP address assignments, requests, or system updates. This feature enhances user experience by providing instant feedback and alerts.

<img width="200" height="80" alt="3" src="https://github.com/user-attachments/assets/49ac48ff-d21c-469a-a537-807fa443faec" />

### Interactive Dashboard  
The interactive dashboard leverages mouse hover and click events, allowing users to view detailed information such as IP address allocation, device types, and user information. This feature provides an intuitive understanding of IP address distribution and system data. 

<img width="300" height="280" alt="4" src="https://github.com/user-attachments/assets/b4c690c7-89a7-4a79-8dec-e6773f68d368" />

## Administrator Features  

### IP Address Calculation  
Administrators can calculate IP addresses based on subnet masks, determining the number of available IP addresses within a subnet and allocating them efficiently. Occupied IP addresses are identified, and the system displays the number of available IP addresses to facilitate effective management.  

<table>
<tr>
<td> <img width="300" height="100" alt="5" src="https://github.com/user-attachments/assets/af9796ac-0d61-4902-ae6a-5cd15d452f1b" /> </td>
<td> <img width="300" height="100" alt="5 5" src="https://github.com/user-attachments/assets/573dfb68-9845-4d1a-a890-04a61863020d" /> </td>
</tr>
</table>

### Assign IP Addresses  
Administrators can assign IP addresses to multiple users simultaneously. Allocation can be based on IP address ranges, user roles, and departments.

<img width="500" height="100" alt="6" src="https://github.com/user-attachments/assets/1e9a308a-a9ba-4086-834b-d9b74acf2612" />

### Staff Query and Assignment  
Administrators can search for staff members and assign IP addresses accordingly. This feature ensures quick and accurate IP address allocation based on roles and departmental needs.  

<img width="700" height="100" alt="7" src="https://github.com/user-attachments/assets/78700134-3895-4e06-a347-544c6c4cad2c" />

### Tracking and Management  
The system tracks and manages all allocated IP addresses and their associated devices. Records include MAC addresses, user names, comments, and device types, ensuring comprehensive management.  

<img width="500" height="100" alt="8" src="https://github.com/user-attachments/assets/9309c327-ce6f-4bcc-9615-bda6c6d0aa85" />

### IP Address Pool Management  
Administrators can manage a pool of available IP addresses, enabling efficient organization and allocation of IP address ranges.  

<img width="500" height="100" alt="9" src="https://github.com/user-attachments/assets/cb520065-d613-4fef-bd10-7b0895913568" />

## User Features  

### IP Address Request  
Users can submit requests for IP address assignments. This feature ensures that users can request IP addresses based on their specific needs.

<img width="600" height="100" alt="10" src="https://github.com/user-attachments/assets/a7b2841a-176c-404b-80ba-72aef557884b" />

### CSV Import and Export  
Users can import and export data using CSV files for detailed IP address management. This functionality supports streamlined data handling for administrators.

<img width="500" height="220" alt="11" src="https://github.com/user-attachments/assets/5f54c6dc-22cb-40b4-97d3-304e1b274fd3" />


## System Architecture  

### Flask Blueprints  
The application is modularized using Flask blueprints, facilitating organized development and maintenance of different components.  

<img width="260" height="140" alt="12" src="https://github.com/user-attachments/assets/a3ed12c7-cdf2-4834-9448-b796200367cf" />


### SOAP API Integration  
SOAP APIs are integrated to retrieve and update data from external sources. This enables seamless communication with external databases and services for data retrieval and updates.  

### MySQL Database  
The system uses MySQL for scalability and future expansion. The database is managed via SQLAlchemy ORM for efficient operations.  

<img width="300" height="180" alt="13" src="https://github.com/user-attachments/assets/f8a79d31-f096-4ce5-9d3a-13ada6b39649" />


### Apache and mod_wsgi Deployment  
The application is deployed using Apache and mod_wsgi, ensuring stability and security.  

### Docker Volumes
The Flask application (Apache/mod_wsgi) and the MySQL database are containerized separately using Docker Compose.

### Low Coupling Design  
A low-coupling design approach enhances code readability and maintainability, making the system easier to extend and debug.

<img width="300" height="180" alt="14" src="https://github.com/user-attachments/assets/2d53007e-4f08-48db-9c7b-79b3ef83b1a3" />

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
