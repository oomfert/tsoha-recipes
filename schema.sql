CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES accounts,
    name TEXT,
    steps TEXT,
    public BOOLEAN,
    visible BOOLEAN
);

CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    name TEXT,
    visible BOOLEAN
);

CREATE TABLE quantities (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes,
    ingredient_id INTEGER REFERENCES ingredients,
    amount TEXT
);