CREATE TABLE users (
    user_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    account_number BIGINT UNIQUE NOT NULL,
    aba VARCHAR(9) NOT NULL,
    contact VARCHAR(15),
    account_type VARCHAR(10) NOT NULL,
    balance DECIMAL(10, 2) NOT NULL
);

-- Sample entries with user_id from 1 to 10
INSERT INTO users (user_id, name, account_number, aba, contact, account_type, balance)
VALUES
    (1, 'John Doe', 12345678, '11122333', '123-456-7890', 'Savings', 0.00),
    (2, 'Jane Smith', 87654321, '98765432', '987-654-3210', 'Current', 0.00),
    (3, 'Alice Johnson', 55558888, '11223344', '555-123-7890', 'Savings', 0.00),
    (4, 'Bob Brown', 99998888, '44556677', '999-888-7777', 'Current', 0.00),
    (5, 'Sarah Miller', 12341234, '11122333', '555-987-6543', 'Savings', 0.75),
    (6, 'Michael Johnson', 56785678, '22233444', '777-123-4567', 'Current', 0.00),
    (7, 'Emily Davis', 98769876, '44556677', '888-555-1234', 'Savings', 0.25),
    (8, 'Robert White', 34563456, '55667788', '333-789-0123', 'Current', 0.50),
    (9, 'Linda Brown', 87658765, '88990011', '444-567-8901', 'Savings', 0.00),
    (10, 'Christopher Lee', 23452345, '11223344', '666-789-0123', 'Current', 0.75);

select * from users;