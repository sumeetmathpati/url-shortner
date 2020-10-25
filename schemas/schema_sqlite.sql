CREATE TABLE users (
    id integer primary key autoincrement,
    username text not null unique,
    password text not null,
    admin boolean not null
);

CREATE TABLE urls (
    id integer primary key autoincrement,
    short_url text,
    long_url text ,
    user_id integer references users(id),
    url_name text,
    unique(long_url, user_id)
);