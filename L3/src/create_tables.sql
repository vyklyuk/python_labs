CREATE TABLE users (
    uid SERIAL NOT NULL, 
    email VARCHAR, 
    password VARCHAR, 
    first_name VARCHAR, 
    last_name VARCHAR, 
    PRIMARY KEY (uid)
);

CREATE TABLE wallets (
    uid SERIAL NOT NULL, 
    name VARCHAR, 
    funds BIGINT, 
    owner_uid INTEGER, 
    PRIMARY KEY (uid), 
    FOREIGN KEY(owner_uid) REFERENCES users (uid)
);

CREATE TABLE transactions (
    uid SERIAL NOT NULL, 
    from_wallet_uid INTEGER, 
    to_wallet_uid INTEGER, 
    amount BIGINT, 
    datetime TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    PRIMARY KEY (uid), 
    FOREIGN KEY(from_wallet_uid) REFERENCES wallets (uid), 
    FOREIGN KEY(to_wallet_uid) REFERENCES wallets (uid)
);
