create table "Rooms"
(
    description varchar not null,
    added   date   not null,
    cost        integer,
    id          serial  not null
        constraint rooms_pk
            primary key
);

alter table "Rooms"
    owner to default_user;

 create table "Bookings"
(
    room_id   integer
        constraint table_name_rooms__fk
            references "Rooms"
            on update cascade on delete cascade,
    date_from date   not null,
    date_to   date   not null,
    id        serial not null
        constraint bookings_pk
            primary key
);

alter table "Bookings"
    owner to default_user;

create unique index bookings_id_uindex
    on "Bookings" (id);