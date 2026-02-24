CREATE TABLE People(
    ID int NOT NULL,
    FName varchar(255) NOT NULL,
    LName varchar(255) NOT NULL,
    age INT,
    PRIMARY KEY (ID)
);

CREATE TABLE Password(
    ID int NOT NULL,
    Password varchar(255) NOT NULL,
    FOREIGN KEY (ID) REFERENCES People(ID)
);

CREATE TABLE contacts(
    ID int NOT NULL,
    Email varchar(255),
    FOREIGN KEY (ID) REFERENCES People(ID)
);

CREATE TABLE organisation(
    OrgID varchar(255),
    ID varchar(255),
    OrgName varchar(255),
    PRIMARY KEY (OrgID)
    FOREIGN KEY (ID) REFERENCES People(ID)
);

CREATE TABLE student(
    ID int,
    StuID int NOT NULL,
    OrgID varchar(255),
    PRIMARY KEY(StuID),
    FOREIGN KEY (ID) REFERENCES People(ID),
    FOREIGN KEY (OrgID) REFERENCES organisation(OrgID)
);

CREATE TABLE teacher(
    ID int,
    teachID int NOT NULL,
    organisation varchar(255),
    PRIMARY KEY(teachID),
    FOREIGN KEY (ID) REFERENCES People(ID)
);

CREATE TABLE classes(
    classID int NOT NULL,
    teachID int,
    PRIMARY KEY (classID),
    FOREIGN KEY (teachID) REFERENCES teacher(teachID)
);

CREATE TABLE class_assigned(
    classID int NOT NULL,
    stuID int NOT NULL,
    PRIMARY KEY (classID, stuID),
    FOREIGN KEY (classID) REFERENCES classes(classID),
    FOREIGN KEY (stuID) REFERENCES student(StuID)
);

