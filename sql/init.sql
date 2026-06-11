CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    course VARCHAR(100)
);

INSERT INTO students (name, course) VALUES ('Chetan', 'Computer Science');
INSERT INTO students (name, course) VALUES ('Manjunath', 'Mathematics');
INSERT INTO students (name, course) VALUES ('Suresh', 'Physics');