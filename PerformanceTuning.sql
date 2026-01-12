#PERFORMANCE Tuning 

#1) List of user with their total debit amount 
SELECT users.user_id, users.name, SUM(transactions.amount) AS total_debit_amount
FROM users
JOIN transactions ON users.user_id = transactions.user_id
WHERE transactions.transaction_type = 'Debit'
GROUP BY users.user_id, users.name
ORDER BY total_debit_amount DESC;
#-------------------------------------------------------------------------------------
#performance tuning on the above query 
-- Create indexes
CREATE INDEX idx_user_id ON users (user_id);
CREATE INDEX idx_transaction_user_id ON transactions (user_id);
CREATE INDEX idx_transaction_type ON transactions (transaction_type);

-- Optimized query
SELECT users.user_id, users.name, SUM(transactions.amount) AS total_debit_amount
FROM users
JOIN transactions ON users.user_id = transactions.user_id
WHERE transactions.transaction_type = 'Debit'
GROUP BY users.user_id, users.name
ORDER BY total_debit_amount DESC;


#-----------------------------------------------------------------------------------------#
#2) Monthly Average Spending per User:
SELECT
    u.user_id,
    u.name,
    AVG(t.amount) AS avg_monthly_spending
FROM
    users u
JOIN
    transactions t ON u.user_id = t.user_id
WHERE
    t.date >= NOW() - INTERVAL 1 MONTH
GROUP BY
    u.user_id;


