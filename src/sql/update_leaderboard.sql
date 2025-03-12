INSERT INTO leaderboard ("user", "count")
VALUES (%s, 1)
ON CONFLICT ("user") DO UPDATE
  SET count = leaderboard.count + 1;