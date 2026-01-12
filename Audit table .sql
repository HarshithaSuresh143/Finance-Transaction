drop table audit;
drop trigger debug_transaction_audit;
CREATE TABLE audit (
    action_type VARCHAR(10),
    user_id INT,
    old_balance DECIMAL(10, 2),
    new_balance DECIMAL(10, 2)
    
);

DELIMITER //
CREATE TRIGGER debug_transaction_audit
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    INSERT INTO audit (action_type, user_id, old_balance, new_balance)
    VALUES ('UPDATE', OLD.user_id, OLD.balance, NEW.balance);
END;
//
DELIMITER ;

select * from audit;