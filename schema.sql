--DROP TABLE IF EXISTS risk;
DROP TABLE IF EXISTS person;

--CREATE TABLE risk (
--    id INTEGER PRIMARY KEY AUTOINCREMENT,
--    owner_id INTEGER references person(id),
--   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--    category TEXT NOT NULL,
--    impact INTEGER NOT NULL,
--    proximity TEXT NOT NULL,
--    response TEXT NOT NULL,
--    status TEXT NOT NULL,
--    contact TEXT NOT NULL,
--    description TEXT NOT NULL
--);

CREATE TABLE person (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    login TEXT NOT NULL,
    password TEXT NOT NULL
);