SELECT hours FROM timesheet WHERE DATE(created_at) >= current_date - interval '7 days' AND person_id = %s;