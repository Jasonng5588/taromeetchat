const { Client } = require('pg');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const DATABASE_URL = "postgresql://postgres.jxregeqaytbcwtrmlweg:55886767%2BaB@aws-1-ap-south-1.pooler.supabase.com:5432/postgres";
const SECRET_KEY = "taromeet-super-secret-key-2024";

module.exports = async (req, res) => {
    // CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ detail: 'Method not allowed' });
    }

    try {
        const { email, username, password } = req.body;

        if (!email || !username || !password) {
            return res.status(400).json({ detail: '缺少必填字段' });
        }

        const client = new Client({ connectionString: DATABASE_URL, ssl: { rejectUnauthorized: false } });
        await client.connect();

        // Check if user exists
        const existing = await client.query('SELECT id FROM users WHERE email = $1', [email]);
        if (existing.rows.length > 0) {
            await client.end();
            return res.status(400).json({ detail: '该邮箱已被注册' });
        }

        // Hash password
        const hashedPassword = await bcrypt.hash(password, 10);

        // Insert user
        const result = await client.query(
            'INSERT INTO users (email, username, hashed_password, is_premium, created_at) VALUES ($1, $2, $3, $4, NOW()) RETURNING id',
            [email, username, hashedPassword, false]
        );

        const userId = result.rows[0].id;
        await client.end();

        // Create JWT
        const token = jwt.sign({ sub: email }, SECRET_KEY, { expiresIn: '7d' });

        return res.status(200).json({
            access_token: token,
            token_type: 'bearer',
            user: {
                id: userId,
                email: email,
                username: username,
                is_premium: false
            }
        });

    } catch (error) {
        console.error('Register error:', error);
        return res.status(500).json({ detail: error.message });
    }
};
