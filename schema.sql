-- Postgres

CREATE TABLE users (
    id serial primary key,
    username text not null unique,
    password text not null,
    admin boolean not null
);