-- insert datasets

-- into table user
INSERT INTO `user` (username, role) VALUES ('Charlie', 'PARENT');
INSERT INTO `user` (username, role) VALUES ('Alice', 'PARENT');
INSERT INTO `user` (username, role) VALUES ('Bob', 'CHILD');
INSERT INTO `user` (username, role) VALUES ('Lisa', 'CHILD');

-- into table activity
INSERT INTO `activity` (activity_name, points) VALUES ('Geschirr waschen', 5);
INSERT INTO `activity` (activity_name, points) VALUES ('Staubsaugen', 3);
INSERT INTO `activity` (activity_name, points) VALUES ('Hausaufgaben machen', 10);
INSERT INTO `activity` (activity_name, points) VALUES ('Pflanze gießen', 2);
INSERT INTO `activity` (activity_name, points) VALUES ('Hiragana üben', 2);