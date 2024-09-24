Description:
This is a full-featured web application developed using the Django framework (Python) with MySQL as the database. The system allows parents to book vaccination appointments for their children at registered hospitals, while hospital staff can manage and approve these appointments. The application provides secure access and user roles, ensuring that only approved hospital staff can manage appointment bookings.

User types:
1) Parents-> Can freely create an account and log in to the system.
Add their child’s details to the system.
Select a hospital and vaccine for their child and request an appointment.
View appointment status (pending, approved, or rejected) and the assigned date and time.
See which hospital staff or doctor has approved the appointment.
Option to edit the appointment, which resets the status to pending for further approval.

2) Hospital Staff-> Can create accounts, but their account status is initially set to "pending".
Admin approval is required to activate hospital staff accounts, ensuring that only authorized staff members can manage appointments.
Once approved, hospital staff can view pending appointments, assign dates and times, and change appointment statuses to "approved" or "rejected".
Staff can also view the details of the child associated with each appointment.

3) Admin->
Admin has control over hospital staff account approvals.
Can update the account status from "pending" to "active," providing a layer of security.

