-- Postgres

CREATE TABLE users (
    id serial primary key,
    username text not null unique,
    password text not null,
    admin boolean not null
);

CREATE TABLE urls (
    id serial PRIMARY KEY,
	short_url text NOT null,
    long_url text NOT null,
	user_id bigint REFERENCES users(id),
	UNIQUE (long_url, user_id)
);