CREATE TABLE users (
    id int primary key autoincrement,
    username text not null unique,
    password text not null,
    admin boolean not null
);

CREATE TABLE urls (
    id int primary key autoincrement,
    short_url text,
    long_url text ,
    user_id int references users(id),
    url_name text,
    unique(long_url, user_id)
)