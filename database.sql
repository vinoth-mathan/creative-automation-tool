BEGIN TRANSACTION;
CREATE TABLE accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );
INSERT INTO "accounts" VALUES(1,'Tata');
INSERT INTO "accounts" VALUES(2,'Volkswagen');
CREATE TABLE dealerships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER,
        name TEXT NOT NULL,
        panel_path TEXT NOT NULL,
        logo_dark_path TEXT,
        logo_light_path TEXT,
        FOREIGN KEY (account_id) REFERENCES accounts (id)
    );
INSERT INTO "dealerships" VALUES(1,1,'Jasper-tata-guntur','assets/Dealership-panels/Tata-dealers/Jasper-tata-guntur/template.png','assets/Dealership-panels/Tata-dealers/Jasper-tata-guntur/logo-dark.png','assets/Dealership-panels/Tata-dealers/Jasper-tata-guntur/logo-light.png');
INSERT INTO "dealerships" VALUES(2,1,'Jasper-tata-hyderabad','assets/Dealership-panels/Tata-dealers/Jasper-tata-hyderabad/template.png','assets/Dealership-panels/Tata-dealers/Jasper-tata-hyderabad/logo-dark.png','assets/Dealership-panels/Tata-dealers/Jasper-tata-hyderabad/logo-light.png');
INSERT INTO "dealerships" VALUES(3,1,'Bellad-tata','assets/Dealership-panels/Tata-dealers/Bellad-tata/template.png','assets/Dealership-panels/Tata-dealers/Bellad-tata/logo-dark.png','assets/Dealership-panels/Tata-dealers/Bellad-tata/logo-light.png');
INSERT INTO "dealerships" VALUES(4,1,'Kaveri-tata','assets/Dealership-panels/Tata-dealers/Kaveri-tata/template.png','assets/Dealership-panels/Tata-dealers/Kaveri-tata/logo-dark.png','assets/Dealership-panels/Tata-dealers/Kaveri-tata/logo-light.png');
INSERT INTO "dealerships" VALUES(5,1,'true-sai','assets/Dealership-panels/Tata-dealers/true-sai/template.png','assets/Dealership-panels/Tata-dealers/true-sai/logo-dark.png','assets/Dealership-panels/Tata-dealers/true-sai/logo-light.png');
INSERT INTO "dealerships" VALUES(6,1,'Shiva-tata','assets/Dealership-panels/Tata-dealers/Shiva-tata/template.png','assets/Dealership-panels/Tata-dealers/Shiva-tata/logo-dark.png','assets/Dealership-panels/Tata-dealers/Shiva-tata/logo-light.png');
INSERT INTO "dealerships" VALUES(7,1,'Jasper-tata-delhi','assets/Dealership-panels/Tata-dealers/Jasper-tata-delhi/template.png','assets/Dealership-panels/Tata-dealers/Jasper-tata-delhi/logo-dark.png','assets/Dealership-panels/Tata-dealers/Jasper-tata-delhi/logo-light.png');
INSERT INTO "dealerships" VALUES(8,1,'Lakshmi-tata','assets/Dealership-panels/Tata-dealers/Lakshmi-tata/template.png','assets/Dealership-panels/Tata-dealers/Lakshmi-tata/logo-dark.png','assets/Dealership-panels/Tata-dealers/Lakshmi-tata/logo-light.png');
INSERT INTO "dealerships" VALUES(9,1,'Jasper-tata-vizag','assets/Dealership-panels/Tata-dealers/Jasper-tata-vizag/template.png','assets/Dealership-panels/Tata-dealers/Jasper-tata-vizag/logo-dark.png','assets/Dealership-panels/Tata-dealers/Jasper-tata-vizag/logo-light.png');
INSERT INTO "dealerships" VALUES(10,1,'Jayaraj-tata','assets/Dealership-panels/Tata-dealers/Jayaraj-tata/template.png','assets/Dealership-panels/Tata-dealers/Jayaraj-tata/logo-dark.png','assets/Dealership-panels/Tata-dealers/Jayaraj-tata/logo-light.png');
INSERT INTO "dealerships" VALUES(11,1,'Jasper-tata-vijayawada','assets/Dealership-panels/Tata-dealers/Jasper-tata-vijayawada/template.png','assets/Dealership-panels/Tata-dealers/Jasper-tata-vijayawada/logo-dark.png','assets/Dealership-panels/Tata-dealers/Jasper-tata-vijayawada/logo-light.png');
INSERT INTO "dealerships" VALUES(12,2,'VW-Apple','assets/Dealership-panels/VW-dealers/VW-Apple/template.png','assets/Dealership-panels/VW-dealers/VW-Apple/logo-dark.png','assets/Dealership-panels/VW-dealers/VW-Apple/logo-light.png');
INSERT INTO "dealerships" VALUES(13,2,'VW-Hubli','assets/Dealership-panels/VW-dealers/VW-Hubli/template.png','assets/Dealership-panels/VW-dealers/VW-Hubli/logo-dark.png','assets/Dealership-panels/VW-dealers/VW-Hubli/logo-light.png');
INSERT INTO "dealerships" VALUES(14,2,'VW-Autobhan','assets/Dealership-panels/VW-dealers/VW-Autobhan/template.png','assets/Dealership-panels/VW-dealers/VW-Autobhan/logo-dark.png','assets/Dealership-panels/VW-dealers/VW-Autobhan/logo-light.png');
INSERT INTO "dealerships" VALUES(15,2,'VW-Jodhpur','assets/Dealership-panels/VW-dealers/VW-Jodhpur/template.png','assets/Dealership-panels/VW-dealers/VW-Jodhpur/logo-dark.png','assets/Dealership-panels/VW-dealers/VW-Jodhpur/logo-light.png');
INSERT INTO "dealerships" VALUES(16,2,'VW-Gorakpur','assets/Dealership-panels/VW-dealers/VW-Gorakpur/template.png','assets/Dealership-panels/VW-dealers/VW-Gorakpur/logo-dark.png','assets/Dealership-panels/VW-dealers/VW-Gorakpur/logo-light.png');
INSERT INTO "dealerships" VALUES(17,2,'VW-Haldawani','assets/Dealership-panels/VW-dealers/VW-Haldawani/template.png','assets/Dealership-panels/VW-dealers/VW-Haldawani/logo-dark.png','assets/Dealership-panels/VW-dealers/VW-Haldawani/logo-light.png');
INSERT INTO "dealerships" VALUES(18,2,'VW-Dehradyun','assets/Dealership-panels/VW-dealers/VW-Dehradyun/template.png','assets/Dealership-panels/VW-dealers/VW-Dehradyun/logo-dark.png','assets/Dealership-panels/VW-dealers/VW-Dehradyun/logo-light.png');
INSERT INTO "dealerships" VALUES(19,2,'VW-Bangalore','assets/Dealership-panels/VW-dealers/VW-Bangalore/template.png','assets/Dealership-panels/VW-dealers/VW-Bangalore/logo-dark.png','assets/Dealership-panels/VW-dealers/VW-Bangalore/logo-light.png');
INSERT INTO "dealerships" VALUES(20,2,'VW-Frontier','assets/Dealership-panels/VW-dealers/VW-Frontier/template.png','assets/Dealership-panels/VW-dealers/VW-Frontier/logo-dark.png','assets/Dealership-panels/VW-dealers/VW-Frontier/logo-light.png');
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('accounts',2);
INSERT INTO "sqlite_sequence" VALUES('dealerships',20);
COMMIT;
