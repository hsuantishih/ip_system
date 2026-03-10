# IP Management System  

This repository contains an IP Management System designed to efficiently organize and manage IP addresses. The system supports two types of user roles: administrators and regular users, each with tailored functionalities.

## General Features  

### Login and Logout Functionality  
The system ensures secure login and logout processes, validated through the school database and robust authentication mechanisms. Access is restricted to current school faculty, staff, and students. User permissions are role-specific, ensuring appropriate access control.

<img src="https://github.com/user-attachments/assets/c518c8cf-9df5-487b-8388-aa484643a6dd" width="300" height="200">

### Search and Filter  
Users can search and filter IP addresses based on various criteria such as IP address, device name, and user name. This functionality enables quick identification of specific IP addresses and devices. 

<img src="https://github.com/user-attachments/assets/219afcb5-6bbc-4c37-85b3-ed21d1c91e75" width="500" height="100">

### Pop-up Notifications  
The system includes real-time pop-up notifications to inform users about important events, such as successful IP address assignments, requests, or system updates. This feature enhances user experience by providing instant feedback and alerts.

<img src="https://github.com/user-attachments/assets/7a61c35e-537f-4c59-9240-ecfc79e7a890" width="200" height="80">

### Interactive Dashboard  
The interactive dashboard leverages mouse hover and click events, allowing users to view detailed information such as IP address allocation, device types, and user information. This feature provides an intuitive understanding of IP address distribution and system data. 

<img src="https://github.com/user-attachments/assets/e801417f-e84b-486a-94b7-10fe658b0fd0" width="300" height="280">

## Administrator Features  

### IP Address Calculation  
Administrators can calculate IP addresses based on subnet masks, determining the number of available IP addresses within a subnet and allocating them efficiently. Occupied IP addresses are identified, and the system displays the number of available IP addresses to facilitate effective management.  

<table>
<tr>
<td> <img src="https://github.com/user-attachments/assets/51f8abb5-1720-48f3-bbd8-0ef4b081ce70" width="300" height="100"> </td>
<td> <img src="https://github.com/user-attachments/assets/8ff8c375-e7f5-4295-b071-f53095b22599" width="380" height="100"> </td>
</tr>
</table>

### Assign IP Addresses  
Administrators can assign IP addresses to multiple users simultaneously. Allocation can be based on IP address ranges, user roles, and departments.

<img src="https://github.com/user-attachments/assets/eeafa414-0572-483e-86b9-bc9d110719df" width="500" height="100">

### Staff Query and Assignment  
Administrators can search for staff members and assign IP addresses accordingly. This feature ensures quick and accurate IP address allocation based on roles and departmental needs.  

<img src="https://github.com/user-attachments/assets/1014a742-588e-48de-ae7e-628653d23e0d" width="700" height="100">

### Tracking and Management  
The system tracks and manages all allocated IP addresses and their associated devices. Records include MAC addresses, user names, comments, and device types, ensuring comprehensive management.  

<img src="https://github.com/user-attachments/assets/6f9cf753-fd97-417b-95c5-6ddc3a23d823" width="500" height="100">

### IP Address Pool Management  
Administrators can manage a pool of available IP addresses, enabling efficient organization and allocation of IP address ranges.  

<img src="https://github.com/user-attachments/assets/33a690f6-69cd-4ed6-9553-364b3a738238" width="500" height="100">

## User Features  

### IP Address Request  
Users can submit requests for IP address assignments. This feature ensures that users can request IP addresses based on their specific needs.  

<img src="https://github.com/user-attachments/assets/845b55cd-75fb-4a5c-be05-9abc606be088" width="600" height="100">

### CSV Import and Export  
Users can import and export data using CSV files for detailed IP address management. This functionality supports streamlined data handling for administrators.  

<img src="https://github.com/user-attachments/assets/08df6039-1ba2-4663-b1d7-1cdba24c6713" width="500" height="220">

## System Architecture  

### Flask Blueprints  
The application is modularized using Flask blueprints, facilitating organized development and maintenance of different components.  

<img src="https://github.com/user-attachments/assets/18d66a39-f072-490d-bb80-5202bacb8a7c" width="260" height="140">

### SOAP API Integration  
SOAP APIs are integrated to retrieve and update data from external sources. This enables seamless communication with external databases and services for data retrieval and updates.  

### MySQL Database  
The system uses MySQL for scalability and future expansion. The database is managed via SQLAlchemy ORM for efficient operations.  

<img src="https://github.com/user-attachments/assets/ca52c920-9c93-4db0-9a09-12ad6ae95b6f" width="300" height="180">

### Apache and mod_wsgi Deployment  
The application is deployed using Apache and mod_wsgi, ensuring stability and security.  

### Docker Volumes
The Flask application (Apache/mod_wsgi) and the MySQL database are containerized separately using Docker Compose.

### Low Coupling Design  
A low-coupling design approach enhances code readability and maintainability, making the system easier to extend and debug.

<img src="https://github.com/user-attachments/assets/0c999649-a87a-44e8-919b-9d14eab1b432" width="300" height="180">

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
