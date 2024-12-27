CREATE TABLE IF NOT EXISTS exhibits(
   exhibit_id INTEGER PRIMARY KEY,
   name TEXT UNIQUE,
   owner TEXT
);
    
CREATE TABLE IF NOT EXISTS exhibitions(
   exhibition_id INTEGER PRIMARY KEY,
   name TEXT UNIQUE,
   description TEXT
);

CREATE TABLE IF NOT EXISTS order_hold(
   order_id INTEGER PRIMARY KEY, 
   date_reg timestamp,
   date_hold timestamp,
   exhibition_id INTEGER,
   place TEXT,
   FOREIGN KEY (exhibition_id) REFERENCES exhibits (exhibitions) ON DELETE CASCADE

);

CREATE TABLE IF NOT EXISTS order_hold_exhibits(
   order_id INTEGER,
   exhibit_id INTEGER,
   PRIMARY KEY (order_id, exhibit_id),
   FOREIGN KEY (order_id) REFERENCES order_hold (order_id) ON DELETE CASCADE,
   FOREIGN KEY (exhibit_id) REFERENCES exhibits (exhibit_id) ON DELETE CASCADE
);
