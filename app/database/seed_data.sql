DELETE FROM doctor_locations;
DELETE FROM doctors;
DELETE FROM locations;
DELETE FROM doctor_schedules;

INSERT INTO doctors(id, first_name, last_name) VALUES (0, 'Jane', 'Wright');
INSERT INTO doctors(id, first_name, last_name) VALUES (1, 'Joseph', 'Lister');

INSERT INTO locations(id, address) VALUES (0, '1 Park St');
INSERT INTO locations(id, address) VALUES (1, '2 University Ave');

INSERT INTO doctor_locations(id, doctor_id, location_id) VALUES (0, 0, 0);
INSERT INTO doctor_locations(id, doctor_id, location_id) VALUES (1, 1, 0);
INSERT INTO doctor_locations(id, doctor_id, location_id) VALUES (2, 1, 1);

-- doctor_schedules
INSERT INTO "doctor_schedules" ("id", "doctor_id", "day_of_week", "start_time", "end_time") VALUES (1, 0, '1', '09:00', '12:00');
INSERT INTO "doctor_schedules" ("id", "doctor_id", "day_of_week", "start_time", "end_time") VALUES (2, 0, '1', '15:00', '18:00');
INSERT INTO "doctor_schedules" ("id", "doctor_id", "day_of_week", "start_time", "end_time") VALUES (3, 0, '2', '10:00', '13:00');
INSERT INTO "doctor_schedules" ("id", "doctor_id", "day_of_week", "start_time", "end_time") VALUES (4, 0, '2', '16:00', '19:00');
INSERT INTO "doctor_schedules" ("id", "doctor_id", "day_of_week", "start_time", "end_time") VALUES (5, 0, '3', '10:00', '13:00');
INSERT INTO "doctor_schedules" ("id", "doctor_id", "day_of_week", "start_time", "end_time") VALUES (6, 0, '3', '16:00', '19:00');
INSERT INTO "doctor_schedules" ("id", "doctor_id", "day_of_week", "start_time", "end_time") VALUES (7, 1, '4', '09:00', '12:00');
INSERT INTO "doctor_schedules" ("id", "doctor_id", "day_of_week", "start_time", "end_time") VALUES (8, 1, '4', '15:00', '18:00');
INSERT INTO "doctor_schedules" ("id", "doctor_id", "day_of_week", "start_time", "end_time") VALUES (9, 1, '5', '09:00', '12:00');
INSERT INTO "doctor_schedules" ("id", "doctor_id", "day_of_week", "start_time", "end_time") VALUES (10, 1, '5', '15:00', '18:00');
INSERT INTO "doctor_schedules" ("id", "doctor_id", "day_of_week", "start_time", "end_time") VALUES (11, 1, '1', '09:00', '12:00');
INSERT INTO "doctor_schedules" ("id", "doctor_id", "day_of_week", "start_time", "end_time") VALUES (12, 1, '1', '15:00', '18:00');
