from PyQt6.QtSql import QSqlQuery, QSqlDatabase


con = QSqlDatabase.addDatabase("QSQLITE")
con.setDatabaseName("calculations/patients.sqlite")
con.open()
sql_query = QSqlQuery()
sql_query.exec(
    """
CREATE TABLE patients(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    firstName VARCHAR(30) NOT NULL,
    lastName VARCHAR(30) NOT NULL,
    DOB DATE
)
    """
)

sql_query2 = QSqlQuery()
sql_query2.exec(
    """
CREATE TABLE vaccines (
    vaccineId INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    hepatiteB_1 DATE,
    hepatiteB_2 DATE,
    hepatiteB_3 DATE,
    hepatiteB_4 DATE,
    hepatiteB_5 DATE,
    penta_1 DATE,
    penta_2 DATE,
    penta_3 DATE,
    penta_4 DATE,
    penta_5 DATE,
    tetra_1 DATE,
    tetra_2 DATE,
    tetra_3 DATE,
    tetra_4 DATE,
    tetra_5 DATE,
    prevnar13_1 DATE,
    prevnar13_2 DATE,
    prevnar13_3 DATE,
    prevnar13_4 DATE,
    prevnar13_5 DATE,
    rota_1 DATE,
    rota_2 DATE,
    rota_3 DATE,
    rota_4 DATE,
    rota_5 DATE,
    meningo_1 DATE,
    meningo_2 DATE,
    meningo_3 DATE,
    meningo_4 DATE,
    meningo_5 DATE,
    priorix_1 DATE,
    priorix_2 DATE,
    priorix_3 DATE,
    priorix_4 DATE,
    priorix_5 DATE,
    varilix_1 DATE,
    varilix_2 DATE,
    varilix_3 DATE,
    varilix_4 DATE,
    varilix_5 DATE,
    hepatiteA_1 DATE,
    hepatiteA_2 DATE,
    hepatiteA_3 DATE,
    hepatiteA_4 DATE,
    hepatiteA_5 DATE,
    typhimVI_1 DATE,
    typhimVI_2 DATE,
    typhimVI_3 DATE,
    typhimVI_4 DATE,
    typhimVI_5 DATE,
    papilomaVirus_1 DATE,
    papilomaVirus_2 DATE,
    papilomaVirus_3 DATE,
    papilomaVirus_4 DATE,
    papilomaVirus_5 DATE,
    autres_1 DATE,
    autres_2 DATE,
    autres_3 DATE,
    autres_4 DATE,
    autres_5 DATE, 
  	patientID INT,
    FOREIGN KEY (patientID) REFERENCES patients(id)
)

    """
)

sql_query3 = QSqlQuery()
sql_query3.exec(
    """
CREATE TABLE examinations (
    examinationID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    date DATE,
    age VARCHAR(3),
    height INT,
    weight INT,
    headCircumference INT,
    bloodPressure VARCHAR(10),
    allergy VARCHAR(300),
    history VARCHAR(300),
    physicalExam VARCHAR(300),
    diagnostic VARCHAR(300),
    treatment VARCHAR(300),
    laboratory VARCHAR(300),
    radiology VARCHAR(300),
   	patientID INT,
    FOREIGN KEY (patientID) REFERENCES patients(id)
)
    """
)
