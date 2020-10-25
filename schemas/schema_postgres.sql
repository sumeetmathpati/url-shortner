-- Postgres

CREATE TABLE users (
    id serial primary key,
    username text not null unique,
    password text not null,
    admin boolean not null
);

CREATE TABLE public.urls
(
    id integer NOT NULL PRIMARY KEY,
    short_url text NOT NULL,
    long_url text NOT NULL,
    user_id bigint references user(id),
    url_name text,
    UNIQUE (long_url, user_id),
)