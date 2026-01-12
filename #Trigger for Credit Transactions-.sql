DROP TRIGGER debit_transaction_trigger;
#Trigger for Credit Transactions:

DELIMITER //

CREATE TRIGGER update_balance_after_credit
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
    IF NEW.transaction_type = 'Credit' THEN
        UPDATE users
        SET balance = balance + NEW.amount
        WHERE user_id = NEW.user_id;
    END IF;
END;
//
DELIMITER ;

#Trigger for Debit Transactions:

DELIMITER //

CREATE TRIGGER debit_transaction_trigger
BEFORE INSERT ON transactions
FOR EACH ROW
BEGIN
    DECLARE current_balance DECIMAL(10, 2);

    -- Check if the transaction is a debit
    IF NEW.transaction_type = 'Debit' THEN
        -- Get the current balance for the user
        SELECT balance INTO current_balance FROM users WHERE user_id = NEW.user_id;

        -- Check if the user has enough balance
        IF current_balance < NEW.amount THEN
            -- Mark the transaction as invalid
            SET NEW.status = 'invalid';
        ELSE
            -- Mark the transaction as valid
            SET NEW.status = 'valid';

            -- Update the balance in the 'users' table
            UPDATE users SET balance = current_balance - NEW.amount WHERE user_id = NEW.user_id;
        END IF;
    END IF;
END;

//

DELIMITER ;



DELIMITER //

CREATE TRIGGER update_status_on_credit
BEFORE INSERT ON transactions
FOR EACH ROW
BEGIN
    IF NEW.transaction_type = 'Credit' THEN
        SET NEW.status = 'valid';
    END IF;
END //

DELIMITER ;






