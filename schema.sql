-- Postgres

CREATE TABLE public.users
(
    id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    username character varying(50) COLLATE pg_catalog."default" NOT NULL,
    password character varying(200) COLLATE pg_catalog."default" NOT NULL,
    admin boolean NOT NULL,
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_username_key UNIQUE (username)
)

CREATE TABLE public.urls
(
    id integer NOT NULL DEFAULT nextval('urls_id_seq'::regclass),
    short_url text COLLATE pg_catalog."default" NOT NULL,
    long_url text COLLATE pg_catalog."default" NOT NULL,
    user_id bigint,
    url_name text COLLATE pg_catalog."default",
    CONSTRAINT urls_pkey PRIMARY KEY (id),
    CONSTRAINT urls_long_url_user_id_key UNIQUE (long_url, user_id),
    CONSTRAINT urls_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)