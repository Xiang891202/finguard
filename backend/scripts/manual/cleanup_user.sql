DELETE FROM refresh_tokens WHERE user_id IN (SELECT id FROM users WHERE email = 'ah891202@gmail.com');
DELETE FROM otp_tokens WHERE email = 'ah891202@gmail.com';
DELETE FROM users WHERE email = 'ah891202@gmail.com';