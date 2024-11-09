CREATE TABLE promotion (
    pid SERIAL PRIMARY KEY,             
    client_email VARCHAR(255) NOT NULL, 
    telephone VARCHAR(20),              
    promotion VARCHAR(255),             
    responded BOOLEAN DEFAULT FALSE   
);


CREATE TABLE transfer (
    sender_id INTEGER NOT NULL,      
    recipient_id INTEGER NOT NULL,       
    amount NUMERIC(10, 2) NOT NULL,       
    date DATE                           
);


CREATE TABLE people (
    pid SERIAL PRIMARY KEY,              
    first_name VARCHAR(100) NOT NULL, 
    last_name VARCHAR(100) NOT NULL,     
    telephone VARCHAR(20),             
    email VARCHAR(255) UNIQUE NOT NULL,  
    city VARCHAR(100),                  
    country VARCHAR(100)                
);

CREATE TABLE device (
    did SERIAL PRIMARY KEY,        
    pid INTEGER NOT NULL REFERENCES people(pid) ON DELETE CASCADE,
    device_type VARCHAR(50) NOT NULL 
);

CREATE TABLE transaction (
    eid SERIAL PRIMARY KEY,             -- This id is use to identify each entry in the transaction, since there are multiple items
    tid INTEGER NOT NULL,               -- use to store the trasaction number, a transaction is an entire purchase             
    item_name VARCHAR(100) NOT NULL,  
    price NUMERIC(10, 2) NOT NULL,     
    price_per_item NUMERIC(10, 2),     
    quantity INTEGER NOT NULL,        
    phone VARCHAR(20),                 
    store VARCHAR(100)                 
);

