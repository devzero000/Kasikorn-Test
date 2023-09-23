UPDATE Persons p
JOIN Address a ON p.PersonID = a.PersonID
SET p.ContractAddress = CONCAT(a.Address1, ' ', a.Address2, ' ', a.Address3);
