CREATE TABLE author(
    id integer not null,
    fullname varchar(255) not null,
    about text,
    books_count integer not null,
    image varchar(255),
    url varchar(255),

    primary key(id)    
);

CREATE TABLE genre(
    id integer not null,
    parent_id integer,
    title varchar(255) not null,
    books_count integer not null,
    url varchar(255) not null,
  
    primary key(id)
);

CREATE TABLE book(
    id integer not null,
    title varchar(255) not null,
    description text not null,
    language varchar(10) not null,
    is_audio boolean not null default false,
    final_price float,
    full_price float,
    currency varchar(10),
    min_age integer not null,
    rating float not null,
    year integer,
    pages integer,
    image varchar(255),
    url varchar(255) not null,

    primary key(id)
);

CREATE TABLE book_author(
    id serial,
    book_id integer not null,
    author_id integer not null,

    constraint unique_book_author unique(book_id, author_id),

    foreign key(book_id) references book(id) on delete cascade,
    foreign key(author_id) references author(id) on delete cascade
);

CREATE TABLE book_genre(
    id serial,
    book_id integer not null,
    genre_id integer not null,

    constraint unique_book_genre unique(book_id, genre_id),

    foreign key(book_id) references book(id) on delete cascade,
    foreign key(genre_id) references genre(id) on delete cascade
);
