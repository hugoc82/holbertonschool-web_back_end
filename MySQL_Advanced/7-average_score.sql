-- 7. Average score
-- Creates a stored procedure ComputeAverageScoreForUser
-- that computes and stores the average score for a given user

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE avg_score FLOAT;

    -- Calcul de la moyenne des scores pour l'utilisateur
    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE corrections.user_id = user_id;

    -- Mise à jour de la table users avec la moyenne calculée
    UPDATE users
    SET average_score = avg_score
    WHERE id = user_id;
END;
//

DELIMITER ;

