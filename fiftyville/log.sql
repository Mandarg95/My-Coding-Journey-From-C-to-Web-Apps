-- Keep a log of any SQL queries you execute as you solve the mystery.

-- see what table i am working with--
.schema

-- To understand what happened on the crime scene--
SELECT description FROM Crime_scene_reports WHERE month = 7 AND day = 28 AND street = 'Humphrey Street';

--According to crime reports there was 3 witness which lead me to interview transcript--
SELECT transcript FROM interviews WHERE year = 2023 AND month = 7 AND day = 28;

--According to a witness one theif call someone for less then minute after the thef--
SELECT caller,id,receiver,duration FROM phone_calls WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60;

--According to a witness theif left scene between 10:15 and 10:25 from bakerys parking lot--
SELECT * FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND activity = 'exit' AND minute < 25 AND minute > 15;

--According to a witness saw the theif before the theft withdraw sone money form near atm--
SELECT * FROM atm_transactions WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';

--To match license plate and try finding phone numbers that match from before--
SELECT * FROM people WHERE license_plate = '0NTHK55' OR license_plate = '322W7JE
' OR license_plate = 'L93JTIZ' OR license_plate = 'G412CB7' OR license_plate = '4328GD8'
 OR license_plate = '6P58WS2' OR license_plate = '94KL13X' OR license_plate = '5P2BI95';

-- According to a witness theif said he/she will take first flight from Fiftyville tomorrow--
SELECT * FROM flights WHERE year = 2023 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1;

-- Checking passport number which person taking which flight--
SELECT * FROM passengers WHERE passport_number = 1695452385 OR passport_number =8294398571 OR passport_number = 3592750733 OR passport_number = 5773159633;

-- Cross checking atm_transections and bank_account --
SELECT * FROM bank_accounts AS bank
JOIN atm_transactions AS atm ON bank.account_number = atm.account_number
WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street';

--finding what passengers are taken flight tomorrow--
SELECT * FROM passengers WHERE flight_id IN
(SELECT id FROM flights WHERE year = 2023 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1);

-- FOUND the theif--
WHERE people.license_plate IN
(SELECT license_plate FROM bakery_security_logs
WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25)AND
people.phone_number IN
(SELECT caller FROM phone_calls
WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60)AND
people.id IN
(SELECT person_id FROM bank_accounts AS bank
JOIN atm_transactions AS atm ON bank.account_number = atm.account_number
WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw')AND
people.passport_number IN
(SELECT passport_number FROM passengers WHERE flight_id IN
(SELECT id FROM flights WHERE year = 2023 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1));


--Found city the theif escaped to --
SELECT city FROM airports WHERE id IN
(SELECT destination_airport_id FROM flights WHERE year = 2023 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1);

--Found the accoumplice name--
SELECT name FROM people WHERE phone_number IN
(SELECT receiver FROM phone_calls WHERE year = 2023 AND month = 7 AND day = 28 AND caller IN
(SELECT phone_number FROM people WHERE name = 'Bruce') AND duration < 60);
