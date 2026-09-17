// Shiptivity Module 3 - SQL queries (SQLite, run against shiptivity.db)
// Kanban Board feature release date: 2018-06-02

// PART 1: Create a SQL query that maps out the daily average users before and after the feature change

// Number of distinct users who logged in each day, labelled before or after the Kanban Board release (2018-06-02).
const dailyActiveUsersByDay = `
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
`;

// Average daily active users before vs after the release (averaged over days with at least one login).
const avgDailyActiveUsersBeforeAfter = `
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
`;

// PART 2: Create a SQL query that indicates the number of status changes by card

// Number of status changes for each card. Card creations (oldStatus is null) and priority-only edits are not counted.
const statusChangesByCard = `
SELECT c.id AS card_id, c.name AS card_name, COUNT(h.cardID) AS status_changes
FROM card c
LEFT JOIN card_change_history h
  ON h.cardID = c.id AND h.oldStatus IS NOT NULL AND h.oldStatus <> h.newStatus
GROUP BY c.id, c.name
ORDER BY status_changes DESC, c.id;
`;

// Number of card status changes (and distinct cards changed) on each day.
const statusChangesByDay = `
SELECT date(timestamp, 'unixepoch') AS day,
       COUNT(*)                     AS status_changes,
       COUNT(DISTINCT cardID)       AS cards_changed
FROM card_change_history
WHERE oldStatus IS NOT NULL AND oldStatus <> newStatus
GROUP BY day ORDER BY day;
`;

module.exports = {
  dailyActiveUsersByDay,
  avgDailyActiveUsersBeforeAfter,
  statusChangesByCard,
  statusChangesByDay,
};
