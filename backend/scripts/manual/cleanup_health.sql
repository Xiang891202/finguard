-- 清空順序：先基因（無 CASCADE 到 profile），再 profile
DELETE FROM user_genetic_tests;
DELETE FROM user_health_profiles;

-- 順手清 OTP 與 refresh（讓你可以乾淨重登）
DELETE FROM otp_tokens WHERE email = 'ah891202@gmail.com';
DELETE FROM refresh_tokens WHERE user_id IN (
    SELECT id FROM users WHERE email = 'ah891202@gmail.com'
);

-- 確認 user 還在（不刪）
SELECT id, email FROM users WHERE email = 'ah891202@gmail.com';