CREATE DATABASE IF NOT EXISTS NU_Volunteering_Hub_DB;
USE NU_Volunteering_Hub_DB;

-- -------------------- Departments -------------------- #
CREATE TABLE Department (
    Department_ID BIGINT PRIMARY KEY AUTO_INCREMENT,
    Department_Name ENUM('CS', 'Math', 'English')
);

-- -------------------- Students -------------------- #
CREATE TABLE Student (
    student_id BIGINT UNIQUE NOT NULL PRIMARY KEY,  
    name VARCHAR(50) NOT NULL, 
    email VARCHAR(50) UNIQUE NOT NULL, 
    hashed_password VARCHAR(255) NOT NULL, 
    year ENUM('Freshman', 'Sophomore', 'Junior', 'Senior') NOT NULL,
    track ENUM('CS', 'BMD', 'AI', 'Cyber Security') NOT NULL,
    cgpa FLOAT NOT NULL,
    strength_areas VARCHAR(500) DEFAULT '',
    Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- -------------------- Doctors -------------------- #
CREATE TABLE Doctor (
    Doctor_ID BIGINT PRIMARY KEY AUTO_INCREMENT, 
    Name VARCHAR(50) NOT NULL, 
    Email VARCHAR(50) UNIQUE NOT NULL, 
    Hashed_Password VARCHAR(255) NOT NULL, 
    Department_ID BIGINT NOT NULL, 
    Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY (Department_ID) REFERENCES Department(Department_ID)
);

-- -------------------- TAs -------------------- #
CREATE TABLE TA (
    TA_ID BIGINT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Hashed_Password VARCHAR(255) NOT NULL,
    Department_ID BIGINT NOT NULL,
    Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Department_ID) REFERENCES Department(Department_ID)
);

-- -------------------- Courses -------------------- #

-- -------------------- Questions -------------------- #
CREATE TABLE Question (
    Question_ID BIGINT PRIMARY KEY AUTO_INCREMENT,
    Question_Type ENUM('Student', 'Doctor/TA', 'Club') NOT NULL,
    Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -------------------- Doctors and TAs section -------------------- #
CREATE TABLE Doctors_and_TAs_section (
    Question_ID BIGINT PRIMARY KEY,
    Assistant_Title VARCHAR(100),
    Doctor_ID BIGINT,
    TA_ID BIGINT,
    FOREIGN KEY (Question_ID) REFERENCES Question(Question_ID),
    FOREIGN KEY (Doctor_ID) REFERENCES Doctor(Doctor_ID),
    FOREIGN KEY (TA_ID) REFERENCES TA(TA_ID)
);



-- -------------------- Posts -------------------- #
CREATE TABLE IF NOT EXISTS Post (
    post_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    student_id BIGINT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    tags VARCHAR(500) DEFAULT '',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_deleted TINYINT(1) DEFAULT 0,
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (post_id) REFERENCES Question(Question_ID)
);

-- Table for Comments
CREATE TABLE IF NOT EXISTS comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_deleted TINYINT(1) DEFAULT 0,
    post_id BIGINT NOT NULL,
    student_id BIGINT NOT NULL,
    parent_id INT,
    FOREIGN KEY (post_id) REFERENCES Post(post_id),
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (parent_id) REFERENCES comments(id)
);

-- -------------------- Tags -------------------- #
CREATE TABLE Tag (
    Tag_ID BIGINT PRIMARY KEY AUTO_INCREMENT,
    Tag_Name VARCHAR(100) UNIQUE NOT NULL
);

-- -------------------- Post-Tag Relationship -------------------- #
CREATE TABLE Post_Tag (
    Post_ID BIGINT NOT NULL,
    Tag_ID BIGINT NOT NULL,
    PRIMARY KEY(Post_ID, Tag_ID),
    FOREIGN KEY (Post_ID) REFERENCES Question(Question_ID),
    FOREIGN KEY (Tag_ID) REFERENCES Tag(Tag_ID)
);



-- -------------------- Student Strength Areas -------------------- #
CREATE TABLE Student_Strength_Tag (
    Student_ID BIGINT NOT NULL,
    Tag_ID BIGINT NOT NULL,
    PRIMARY KEY(Student_ID, Tag_ID),
    FOREIGN KEY (Student_ID) REFERENCES Student(student_id),
    FOREIGN KEY (Tag_ID) REFERENCES Tag(Tag_ID)
);

CREATE TABLE Report (
    Report_ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    Post_ID BIGINT NOT NULL,  
    Reporter_Type ENUM('Student', 'Doctor', 'TA') NOT NULL,
    Reporter_ID BIGINT NOT NULL,  
    Reason TEXT NOT NULL,
    Report_Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Status ENUM('Pending','Reviewed','Resolved') DEFAULT 'Pending',
    FOREIGN KEY (Post_ID) REFERENCES Question(Question_ID)
);

