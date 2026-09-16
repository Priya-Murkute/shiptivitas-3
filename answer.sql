-- TYPE YOUR SQL QUERY BELOW

-- PART 1: Create a SQL query that maps out the daily average users before and after the feature change

Select date(
    login_timestamp, 'unixepoch') AS day,
    COUNT(DISTINCT user_id) AS daily_active_users,
    CASE 
        WHEN date(login_timestamp, 'unixepoch') < '2018-06-02' 
            THEN 'Before Feature Change'
        ELSE 'After Feature Change'
    END AS period
FROM login_history
GROUP BY day
ORDER BY day;

-- Average daily active users before vs after (averaged over days with at least one login)
WITH daily AS (
    SELECT date(login_timestamp, 'unixepoch') AS day,
        COUNT(DISTINCT user_id) AS daily_active_users,
        CASE
            WHEN date(login_timestamp, 'unixepoch') < '2018-06-02'
                THEN 'Before Feature Change'
            ELSE 'After Feature Change'
        END AS period
    FROM login_history
    GROUP BY day
)
SELECT period, ROUND(AVG(daily_active_users), 2) AS avg_daily_active_users,
       COUNT(*) AS active_days
FROM daily GROUP BY period ORDER BY period DESC;

-- PART 2: Create a SQL query that indicates the number of status changes by card

SELECT c.id AS card_id, c.name AS card_name, COUNT(h.cardID) AS status_changes
FROM card c
LEFT JOIN card_change_history h
  ON h.cardID = c.id AND h.oldStatus IS NOT NULL AND h.oldStatus <> h.newStatus
GROUP BY c.id, c.name
ORDER BY status_changes DESC, c.id;


SELECT date(timestamp, 'unixepoch') AS day,
       COUNT(*)                     AS status_changes,
       COUNT(DISTINCT cardID)       AS cards_changed
FROM card_change_history
WHERE oldStatus IS NOT NULL AND oldStatus <> newStatus
GROUP BY day ORDER BY day;
