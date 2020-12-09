CREATE TABLE users (
    id INT NOT NULL ,
    name VARCHAR NOT NULL,
    passport VARCHAR NOT NULL,
    address VARCHAR NOT NULL,
    email VARCHAR(100) ,
    phone_number VARCHAR(20) NOT NULL,
    money_amount INT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE banks (
    id INT NOT NULL,
    all_money INT CHECK (all_money between 0 and 517000) NOT NULL,
    per_cent INT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE credits (
    id INT NOT NULL,
    start_date VARCHAR NOT NULL,
    end_date VARCHAR NOT NULL,
    start_sum INT NOT NULL,
    current_sum INT NOT NULL,
    bank_id INT NOT NULL,
    FOREIGN KEY (bank_id) REFERENCES banks(id),
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    PRIMARY KEY (id)
);

CREATE TABLE transactions (
    id INT NOT NULL,
    date DATE NOT NULL,
    summ INT NOT NULL,
    credit_id INT NOT NULL,
    FOREIGN KEY (credit_id) REFERENCES credits(id),
    PRIMARY KEY (id)
);

