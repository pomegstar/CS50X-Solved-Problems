-- Finding crime scene description
SELECT description
FROM crime_scene_reports
WHERE year = 2023 AND month = 7
AND day = 28 AND street = 'Humphrey Street';



-- Finding interviews to get some clue
SELECT transcript
FROM interviews
WHERE year >= 2023
AND month >= 7
AND day >= 28;


--Information after taking intrviews:

-- 1. Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
-- If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.

-- 2. I don't know the thief's name, but it was someone I recognized. Earlier this morning,
-- before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

-- 3. As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call,
--  I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
--  The thief then asked the person on the other end of the phone to purchase the flight ticket.


-- Finding people.id based on cars license_plate that left the parking lot after theft time
WITH cid AS (
    SELECT people.id FROM people
    JOIN bakery_security_logs b ON people.license_plate = b.license_plate
    WHERE b.year = 2023
    AND b.month = 7
    AND b.day = 28
    AND b.hour = 10
    AND b.minute <= 25
    AND b.activity = 'exit'),

    --Finding person_id based on atm_transaction
    aid AS(
    SELECT bank_accounts.person_id
    FROM bank_accounts
    JOIN atm_transactions a ON bank_accounts.account_number = a.account_number
    WHERE a.year = 2023
    AND a.month = 7
    AND a.day = 28
    AND a.atm_location = 'Leggett Street'
    AND a.transaction_type = 'withdraw'),

    -- Finding caller and receiver based on phone_calls
    clr_rcvr AS(
    SELECT phone_calls.caller,phone_calls.receiver
    FROM phone_calls
    WHERE phone_calls.year = 2023
    AND phone_calls.month = 7
    AND phone_calls.day = 28
    AND phone_calls.duration < 60),

    -- Finding flights.id and flights destination airport id after 28 July from fiftyville city
    fid AS(
    SELECT flights.id,flights.destination_airport_id FROM flights
    JOIN airports ON airports.id = flights.origin_airport_id
    WHERE airports.city = 'Fiftyville'
    AND flights.year = 2023
    AND flights.month = 7
    AND flights.day = 29
    ORDER BY flights.hour, flights.minute LIMIT 1),

    --Finding the city where the thief escaped to.
    fid2 AS (
        SELECT city FROM airports
        JOIN fid f ON airports.id = f.destination_airport_id
    )


-- Final result
SELECT p1.name, p2.name, fid2.city
FROM people p1, people p2, fid2, fid
JOIN cid c1 ON c1.id = p1.id
JOIN aid a1 ON a1.person_id = p1.id
JOIN clr_rcvr clr ON clr.caller = p1.phone_number AND clr.receiver = p2.phone_number
WHERE p1.id IN (
    SELECT people.id FROM people
    JOIN passengers ON passengers.passport_number = people.passport_number
    JOIN fid ON fid.id = passengers.flight_id
);

