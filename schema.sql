-- -------------------------------------------------------------
-- TablePlus 5.1.0(468)
--
-- https://tableplus.com/
--
-- Database: prod
-- Generation Time: 2022-12-17 23:17:03.5040
-- -------------------------------------------------------------


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


CREATE TABLE "Appointments" (
  "Appointment_ID" int NOT NULL AUTO_INCREMENT,
  "Schedule_ID" int DEFAULT NULL,
  "Patient_ID" int DEFAULT NULL,
  "Type" varchar(255) DEFAULT NULL,
  "Status" int NOT NULL DEFAULT '1' COMMENT '1=Active, 0 = Canceled',
  "Note" varchar(255) DEFAULT NULL,
  "Create_Date" timestamp NULL DEFAULT NULL,
  PRIMARY KEY ("Appointment_ID"),
  KEY "ix_Appointments_Schedule_ID" ("Schedule_ID"),
  KEY "ix_Appointments_Patient_ID" ("Patient_ID"),
  CONSTRAINT "Appointments_ibfk_1" FOREIGN KEY ("Schedule_ID") REFERENCES "Availability_Schedule" ("Schedule_ID"),
  CONSTRAINT "Appointments_ibfk_2" FOREIGN KEY ("Patient_ID") REFERENCES "Patients" ("Patient_ID")
);

CREATE TABLE "Availability_Schedule" (
  "Schedule_ID" int NOT NULL AUTO_INCREMENT,
  "Schedule_Date" date DEFAULT NULL,
  "Slot_ID" int NOT NULL,
  "Staff_ID" int NOT NULL,
  "Room_ID" int DEFAULT NULL,
  "Status" int DEFAULT '1' COMMENT '1 = Active\n0 = Removed',
  PRIMARY KEY ("Schedule_ID"),
  KEY "ix_Availability_Schedule_Slot_ID" ("Slot_ID"),
  KEY "ix_Availability_Schedule_Room_ID" ("Room_ID"),
  KEY "ix_Availability_Schedule_Staff_ID" ("Staff_ID"),
  CONSTRAINT "Availability_Schedule_ibfk_1" FOREIGN KEY ("Slot_ID") REFERENCES "Time_Slots" ("Slot_ID") ON DELETE RESTRICT,
  CONSTRAINT "Availability_Schedule_ibfk_2" FOREIGN KEY ("Staff_ID") REFERENCES "Hospital_Staff" ("Staff_ID"),
  CONSTRAINT "Availability_Schedule_ibfk_3" FOREIGN KEY ("Room_ID") REFERENCES "Rooms" ("Room_ID")
);

CREATE TABLE "Diagnoses" (
  "Diagnose_ID" int NOT NULL AUTO_INCREMENT,
  "Staff_ID" int DEFAULT NULL,
  "Patient_ID" int DEFAULT NULL,
  "Disease_ID" int DEFAULT NULL,
  "Date_Created" timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  "Note" varchar(255) DEFAULT NULL,
  PRIMARY KEY ("Diagnose_ID"),
  KEY "ix_Diagnoses_Disease_ID" ("Disease_ID"),
  KEY "ix_Diagnoses_Patient_ID" ("Patient_ID"),
  KEY "Diagnoses_FK" ("Staff_ID"),
  CONSTRAINT "Diagnoses_FK" FOREIGN KEY ("Staff_ID") REFERENCES "Hospital_Staff" ("Staff_ID"),
  CONSTRAINT "Diagnoses_ibfk_1" FOREIGN KEY ("Patient_ID") REFERENCES "Patients" ("Patient_ID"),
  CONSTRAINT "Diagnoses_ibfk_3" FOREIGN KEY ("Disease_ID") REFERENCES "Diseases" ("Disease_ID")
);

CREATE TABLE "Diseases" (
  "Disease_ID" int NOT NULL AUTO_INCREMENT,
  "Disease_Name" varchar(255) DEFAULT NULL,
  PRIMARY KEY ("Disease_ID")
);

CREATE TABLE "Hospital_Staff" (
  "Staff_ID" int NOT NULL AUTO_INCREMENT,
  "Name" varchar(255) DEFAULT NULL,
  "Surname" varchar(255) DEFAULT NULL,
  "Specification_ID" int DEFAULT NULL,
  "Role" int DEFAULT NULL,
  "EMail" varchar(255) DEFAULT NULL,
  "Password" varchar(255) DEFAULT NULL,
  "Document_Number" varchar(255) DEFAULT NULL,
  "Country" varchar(255) DEFAULT NULL,
  "City" varchar(255) DEFAULT NULL,
  "Address" varchar(255) DEFAULT NULL,
  "Phone" varchar(255) DEFAULT NULL,
  PRIMARY KEY ("Staff_ID"),
  KEY "ix_Hospital_Staff_Role" ("Role"),
  KEY "ix_Hospital_Staff_Specification_ID" ("Specification_ID"),
  CONSTRAINT "Hospital_Staff_ibfk_1" FOREIGN KEY ("Specification_ID") REFERENCES "Specifications" ("Specification_ID"),
  CONSTRAINT "Hospital_Staff_ibfk_2" FOREIGN KEY ("Role") REFERENCES "Roles" ("Role")
);

CREATE TABLE "Invoice_Records" (
  "Record_ID" int NOT NULL AUTO_INCREMENT,
  "Invoice_Number" int DEFAULT NULL,
  "Staff_ID" int DEFAULT NULL,
  "Description" varchar(255) DEFAULT NULL,
  "Amount" decimal(10,2) DEFAULT NULL,
  "Create_Date" timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY ("Record_ID"),
  KEY "ix_Invoice_Records_Invoice_Number" ("Invoice_Number"),
  KEY "ix_Invoice_Records_Staff_ID" ("Staff_ID"),
  CONSTRAINT "Invoice_Records_ibfk_1" FOREIGN KEY ("Invoice_Number") REFERENCES "Invoices" ("Invoice_Number"),
  CONSTRAINT "Invoice_Records_ibfk_2" FOREIGN KEY ("Staff_ID") REFERENCES "Hospital_Staff" ("Staff_ID")
);

CREATE TABLE "Invoices" (
  "Invoice_Number" int NOT NULL AUTO_INCREMENT,
  "Patient_ID" int DEFAULT NULL,
  "Due_Date" datetime DEFAULT NULL,
  "Status" int DEFAULT NULL,
  "Creation_Date" timestamp NULL DEFAULT NULL,
  PRIMARY KEY ("Invoice_Number"),
  KEY "ix_Invoices_Patient_ID" ("Patient_ID"),
  CONSTRAINT "Invoices_ibfk_1" FOREIGN KEY ("Patient_ID") REFERENCES "Patients" ("Patient_ID")
);

CREATE TABLE "Medicines" (
  "Medicine_ID" int NOT NULL AUTO_INCREMENT,
  "Name" varchar(255) DEFAULT NULL,
  "Barcode" varchar(120) DEFAULT NULL,
  PRIMARY KEY ("Medicine_ID")
);

CREATE TABLE "Patients" (
  "Patient_ID" int NOT NULL AUTO_INCREMENT,
  "Name" varchar(255) DEFAULT NULL,
  "Surname" varchar(255) DEFAULT NULL,
  "Birthdate" datetime DEFAULT NULL,
  "Photo" varchar(255) DEFAULT NULL,
  "Password" varchar(255) DEFAULT NULL,
  "E_Mail" varchar(255) DEFAULT NULL,
  "Status" int DEFAULT NULL,
  "Document_Number" varchar(255) DEFAULT NULL,
  PRIMARY KEY ("Patient_ID")
);

CREATE TABLE "Payments" (
  "Payment_ID" int NOT NULL AUTO_INCREMENT,
  "Invoice_Number" int DEFAULT NULL,
  "Description" varchar(255) DEFAULT NULL,
  "Payment_Date" timestamp NULL DEFAULT NULL,
  "Payment_Amount" decimal(10,2) DEFAULT NULL,
  "Staff_ID" int DEFAULT NULL,
  "Type" varchar(255) DEFAULT NULL,
  PRIMARY KEY ("Payment_ID"),
  KEY "ix_Payments_Invoice_Number" ("Invoice_Number"),
  KEY "Staff_ID" ("Staff_ID"),
  CONSTRAINT "Payments_ibfk_1" FOREIGN KEY ("Invoice_Number") REFERENCES "Invoices" ("Invoice_Number"),
  CONSTRAINT "Payments_ibfk_2" FOREIGN KEY ("Staff_ID") REFERENCES "Hospital_Staff" ("Staff_ID")
);

CREATE TABLE "Prescription_Content" (
  "PRecord_ID" int NOT NULL AUTO_INCREMENT,
  "Prescription_ID" int DEFAULT NULL,
  "Medicine_ID" int DEFAULT NULL,
  "Box" int DEFAULT NULL,
  PRIMARY KEY ("PRecord_ID"),
  KEY "ix_Prescription_Content_Medicine_ID" ("Medicine_ID"),
  KEY "ix_Prescription_Content_Prescription_ID" ("Prescription_ID"),
  CONSTRAINT "Prescription_Content_ibfk_1" FOREIGN KEY ("Prescription_ID") REFERENCES "Prescriptions" ("Prescription_ID"),
  CONSTRAINT "Prescription_Content_ibfk_2" FOREIGN KEY ("Medicine_ID") REFERENCES "Medicines" ("Medicine_ID")
);

CREATE TABLE "Prescriptions" (
  "Prescription_ID" int NOT NULL AUTO_INCREMENT,
  "Patient_ID" int DEFAULT NULL,
  "Staff_ID" int DEFAULT NULL,
  "Description" varchar(255) DEFAULT NULL,
  "Prescription_Date" datetime DEFAULT NULL,
  "Status" int DEFAULT '1',
  PRIMARY KEY ("Prescription_ID"),
  KEY "ix_Prescriptions_Staff_ID" ("Staff_ID"),
  KEY "ix_Prescriptions_Patient_ID" ("Patient_ID"),
  CONSTRAINT "Prescriptions_ibfk_1" FOREIGN KEY ("Patient_ID") REFERENCES "Patients" ("Patient_ID"),
  CONSTRAINT "Prescriptions_ibfk_2" FOREIGN KEY ("Staff_ID") REFERENCES "Hospital_Staff" ("Staff_ID")
);

CREATE TABLE "Roles" (
  "Role" int NOT NULL AUTO_INCREMENT,
  "Description" varchar(255) DEFAULT NULL,
  PRIMARY KEY ("Role")
);

CREATE TABLE "Room_Bookings" (
  "Booking_ID" int NOT NULL AUTO_INCREMENT,
  "Patient_ID" int DEFAULT NULL,
  "Room_ID" int DEFAULT NULL,
  "Start_Date" datetime DEFAULT NULL,
  "End_Date" datetime DEFAULT NULL,
  "Status" int DEFAULT NULL COMMENT '1 = Active, 0 = Cancelled',
  PRIMARY KEY ("Booking_ID"),
  KEY "ix_Room_Bookings_Room_ID" ("Room_ID"),
  KEY "ix_Room_Bookings_Patient_ID" ("Patient_ID"),
  CONSTRAINT "Room_Bookings_ibfk_1" FOREIGN KEY ("Patient_ID") REFERENCES "Patients" ("Patient_ID"),
  CONSTRAINT "Room_Bookings_ibfk_2" FOREIGN KEY ("Room_ID") REFERENCES "Rooms" ("Room_ID")
);

CREATE TABLE "Rooms" (
  "Room_ID" int NOT NULL AUTO_INCREMENT,
  "Room" varchar(255) DEFAULT NULL,
  "Building" varchar(255) DEFAULT NULL,
  "Type" varchar(255) DEFAULT NULL,
  "Status" int DEFAULT '1',
  PRIMARY KEY ("Room_ID")
);

CREATE TABLE "Specifications" (
  "Specification_ID" int NOT NULL AUTO_INCREMENT,
  "Title" varchar(255) DEFAULT NULL,
  PRIMARY KEY ("Specification_ID")
);

CREATE TABLE "System_Config" (
  "Hospital_Name" varchar(255) NOT NULL,
  "Hospital_Address" varchar(255) DEFAULT NULL,
  "Admin_E-Mail" varchar(255) DEFAULT NULL,
  "Admin_Password" varchar(255) DEFAULT NULL,
  "Currency" varchar(255) DEFAULT NULL,
  PRIMARY KEY ("Hospital_Name")
);

CREATE TABLE "Time_Slots" (
  "Slot_ID" int NOT NULL AUTO_INCREMENT,
  "Start_Time" time DEFAULT NULL,
  "End_Time" time DEFAULT NULL,
  PRIMARY KEY ("Slot_ID")
);







CREATE VIEW "V_Appointments" AS select "a"."Appointment_ID" AS "Appointment_ID","a"."Patient_ID" AS "Patient_ID","a"."Status" AS "Status","a"."Type" AS "Type","b"."Schedule_Date" AS "Schedule_Date","b"."Schedule_ID" AS "Schedule_ID","c"."Start_Time" AS "Start_Time","c"."End_Time" AS "End_Time",concat("d"."Name",' ',"d"."Surname") AS "Staff_Name","d"."Staff_ID" AS "Staff_ID","f"."Title" AS "Specification",concat("h"."Building",'-',"h"."Room") AS "Room",concat("e"."Name",' ',"e"."Surname") AS "Patient_Name" from (((((("Appointments" "a" join "Availability_Schedule" "b" on(("a"."Schedule_ID" = "b"."Schedule_ID"))) join "Time_Slots" "c" on(("b"."Slot_ID" = "c"."Slot_ID"))) join "Hospital_Staff" "d" on(("b"."Staff_ID" = "d"."Staff_ID"))) left join "Patients" "e" on(("a"."Patient_ID" = "e"."Patient_ID"))) join "Specifications" "f" on(("d"."Specification_ID" = "f"."Specification_ID"))) join "Rooms" "h" on(("b"."Room_ID" = "h"."Room_ID")));
CREATE VIEW "V_Available_Slots" AS select "a"."Schedule_ID" AS "Schedule_ID","a"."Schedule_Date" AS "Schedule_Date","b"."Start_Time" AS "Start_Time","b"."End_Time" AS "End_Time","d"."Title" AS "Specifications",concat("c"."Name",' ',"c"."Surname") AS "Doctor_Name","c"."Staff_ID" AS "Doctor_ID" from (((("Availability_Schedule" "a" join "Time_Slots" "b" on(("a"."Slot_ID" = "b"."Slot_ID"))) join "Hospital_Staff" "c" on(("a"."Staff_ID" = "c"."Staff_ID"))) join "Specifications" "d" on(("c"."Specification_ID" = "d"."Specification_ID"))) join "Roles" "e" on(("c"."Role" = "e"."Role"))) where ("a"."Schedule_ID" in (select "Appointments"."Schedule_ID" from "Appointments" where ("Appointments"."Status" = 1)) is false and ("e"."Description" = 'Doctor'));
CREATE VIEW "V_Invoices" AS with "Invoice_Summary" as (select "a"."Invoice_Number" AS "Invoice_Number","a"."Creation_Date" AS "Creation_Date","a"."Due_Date" AS "Due_Date","c"."Patient_ID" AS "Patient_ID",concat("c"."Name",' ',"c"."Surname") AS "Patient",sum("b"."Amount") AS "Total_Amount",ifnull(sum("d"."Payment_Amount"),0) AS "Paid_Amount",(sum("b"."Amount") - ifnull(sum("d"."Payment_Amount"),0)) AS "Remaining" from ((("Invoices" "a" left join "Invoice_Records" "b" on(("a"."Invoice_Number" = "b"."Invoice_Number"))) left join "Patients" "c" on(("a"."Patient_ID" = "c"."Patient_ID"))) left join "Payments" "d" on(("a"."Invoice_Number" = "d"."Invoice_Number"))) group by "a"."Invoice_Number") select "Invoice_Summary"."Invoice_Number" AS "Invoice_Number","Invoice_Summary"."Creation_Date" AS "Creation_Date","Invoice_Summary"."Due_Date" AS "Due_Date","Invoice_Summary"."Patient_ID" AS "Patient_ID","Invoice_Summary"."Patient" AS "Patient","Invoice_Summary"."Total_Amount" AS "Total_Amount","Invoice_Summary"."Paid_Amount" AS "Paid_Amount","Invoice_Summary"."Remaining" AS "Remaining",(case when ("Invoice_Summary"."Remaining" = 0) then '1' when ("Invoice_Summary"."Remaining" >= 0) then '0' else "Invoice_Summary"."Remaining" end) AS "Status" from "Invoice_Summary";


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
