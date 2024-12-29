CREATE TABLE IF NOT EXISTS exhibits(
   exhibit_id INTEGER PRIMARY KEY,
   name TEXT,
   owner TEXT,
   status INTEGER
);
    
CREATE TABLE IF NOT EXISTS exhibitions(
   exhibition_id INTEGER PRIMARY KEY,
   name TEXT UNIQUE,
   description TEXT
);

CREATE TABLE IF NOT EXISTS order_hold(
   order_id INTEGER PRIMARY KEY, 
   date_reg timestamp,
   exhibition_id INTEGER,
   place TEXT,
   FOREIGN KEY (exhibition_id) REFERENCES exhibits (exhibitions) ON DELETE CASCADE

);

CREATE TABLE IF NOT EXISTS order_hold_dates(
   order_id INTEGER,
   date_hold timestamp,
   FOREIGN KEY (order_id) REFERENCES order_hold (order_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS order_hold_exhibits(
   order_id INTEGER,
   exhibit_id INTEGER,
   PRIMARY KEY (order_id, exhibit_id),
   FOREIGN KEY (order_id) REFERENCES order_hold (order_id) ON DELETE CASCADE,
   FOREIGN KEY (exhibit_id) REFERENCES exhibits (exhibit_id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS order_get(
   id INTEGER PRIMARY KEY,
   date_get timestamp,
   order_id INTEGER,
   FOREIGN KEY (order_id) REFERENCES order_hold (order_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS order_give(
   id INTEGER PRIMARY KEY,
   date_give timestamp,
   order_id INTEGER,
   FOREIGN KEY (order_id) REFERENCES order_hold (order_id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS order_return(
   id INTEGER PRIMARY KEY,
   date_return timestamp,
   order_id INTEGER,
   FOREIGN KEY (order_id) REFERENCES order_hold (order_id) ON DELETE CASCADE
);
