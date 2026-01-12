#Sheet 1 Count the no of invalid transaction per user 
SELECT users.user_id, users.name, COUNT(transactions.transaction_id) AS total_invalid_transactions
FROM users
JOIN transactions ON users.user_id = transactions.user_id
WHERE transactions.status = 'invalid'
GROUP BY users.user_id, users.name;

#Sheet 2 : Total no of transaction for each category for user 1 
SELECT users.user_id, users.name, transactions.category, COUNT(transactions.transaction_id) AS total_transactions
FROM users
JOIN transactions ON users.user_id = transactions.user_id
WHERE users.user_id = 1
GROUP BY users.user_id, users.name, transactions.category;

#Sheet 3 : count the total number of transactions for Category = beauty per user ,
SELECT users.user_id, users.name, COUNT(transactions.transaction_id) AS total_transactions
FROM users
JOIN transactions ON users.user_id = transactions.user_id
WHERE transactions.category = 'Beauty'
GROUP BY users.user_id, users.name;

