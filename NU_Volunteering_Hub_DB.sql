CREATE DATABASE IF NOT EXISTS NU_Volunteering_Hub;
USE NU_Volunteering_Hub;

CREATE TABLE Department (
	Department_ID INT PRIMARY KEY AUTO_INCREMENT,
    Department_Name ENUM("CS", "Math", "English")
);

CREATE TABLE Student (
	Student_ID INT PRIMARY KEY,  
    Name VARCHAR(50) NOT NULL, 
    Email VARCHAR(30) UNIQUE NOT NULL, 
    Hashed_Password VARCHAR(255) NOT NULL, 
    Student_Year ENUM("Freshman", "Sophomore", "Junior", "Senior") NOT NULL,
    Track ENUM("CS", "BMD", "AI", "Cyber Security") NOT NULL,
    Research_Skill ENUM("Yes", "No") NOT NULL, 
    JTA ENUM("Yes", "No"),
    CGPA FLOAT NOT NULL,
    Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Doctor (
	Doctor_ID INT PRIMARY KEY AUTO_INCREMENT, 
    Name VARCHAR(50) NOT NULL, 
    Email VARCHAR(30) UNIQUE NOT NULL, 
    Hashed_Password VARCHAR(255) NOT NULL, 
    Department_ID INT NOT NULL, 
    Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY (Department_ID) REFERENCES Department(Department_ID)
);

CREATE TABLE TA (
    TA_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Hashed_Password VARCHAR(255) NOT NULL,
    Department_ID INT NOT NULL,
    Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Department_ID) REFERENCES Department(Department_ID)
);

CREATE TABLE Question (
    Question_ID INT PRIMARY KEY AUTO_INCREMENT,
    Question_Type ENUM('Student', 'Doctor/TA', 'Club') NOT NULL,
    Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Course (
    Course_ID INT PRIMARY KEY AUTO_INCREMENT,
    Course_Name VARCHAR(100) NOT NULL
);

CREATE TABLE Student_Question (
    Question_ID INT PRIMARY KEY,  -- PK + FK to Question
    Questioner_ID INT NOT NULL,
    Course_ID INT NOT NULL,
    Department_ID INT NOT NULL,
    Question_Text TEXT NOT NULL,
    FOREIGN KEY (Question_ID) REFERENCES Question(Question_ID),
    FOREIGN KEY (Questioner_ID) REFERENCES Student(Student_ID),
    FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID),
    FOREIGN KEY (Department_ID) REFERENCES Department(Department_ID)
);

CREATE TABLE Doctors_and_TAs_section (
    Question_ID INT PRIMARY KEY,  -- PK + FK to Question
    Assistant_Title VARCHAR(100),
    Doctor_ID INT,
    TA_ID INT,
    FOREIGN KEY (Question_ID) REFERENCES Question(Question_ID),
    FOREIGN KEY (Doctor_ID) REFERENCES Doctor(Doctor_ID),
    FOREIGN KEY (TA_ID) REFERENCES TA(TA_ID)
);

CREATE TABLE Club (
    Club_ID INT PRIMARY KEY AUTO_INCREMENT,
	Club_Email VARCHAR(100) UNIQUE NOT NULL,
    Hashed_Password VARCHAR(255) NOT NULL,
    Club_Name VARCHAR(100) NOT NULL,
    Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Club_Post (
    Question_ID INT PRIMARY KEY,  -- PK + FK to Question
    Club_ID INT NOT NULL,
    Post_Text TEXT NOT NULL,
    FOREIGN KEY (Question_ID) REFERENCES Question(Question_ID),
    FOREIGN KEY (Club_ID) REFERENCES Club(Club_ID)
);

CREATE TABLE Response (
    Response_ID INT PRIMARY KEY AUTO_INCREMENT,
    Question_ID INT NOT NULL,
    Responder_ID INT NOT NULL,
    Response_Text TEXT NOT NULL,
    Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Question_ID) REFERENCES Question(Question_ID)
);

