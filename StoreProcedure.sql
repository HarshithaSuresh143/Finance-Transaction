drop procedure GetAuditTrail;
#create stored procedure to fetch audit trail for a given user
DELIMITER //

CREATE PROCEDURE GetAuditTrail(IN p_user_id INT)
BEGIN
    SELECT
        action_type,
        user_id,
        old_balance,
        new_balance
    FROM
        audit
    WHERE
        user_id = p_user_id;
END //

DELIMITER ;

CALL GetAuditTrail(1);



