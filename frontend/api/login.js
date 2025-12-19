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
        let email, password;

        // Parse form data or JSON
        const contentType = req.headers['content-type'] || '';
        if (contentType.includes('application/x-www-form-urlencoded')) {
            email = req.body.username;  // OAuth2 format uses 'username'
            password = req.body.password;
        } else {
            email = req.body.email || req.body.username;
            password = req.body.password;
        }

        if (!email || !password) {
            return res.status(400).json({ detail: '缺少邮箱或密码' });
        }

        const client = new Client({ connectionString: DATABASE_URL, ssl: { rejectUnauthorized: false } });
        await client.connect();

        // Get user
        const result = await client.query(
            'SELECT id, email, username, hashed_password, is_premium FROM users WHERE email = $1',
            [email]
        );

        if (result.rows.length === 0) {
            await client.end();
            return res.status(401).json({ detail: '邮箱或密码错误' });
        }

        const user = result.rows[0];
        await client.end();

        // Verify password
        const valid = await bcrypt.compare(password, user.hashed_password);
        if (!valid) {
            return res.status(401).json({ detail: '邮箱或密码错误' });
        }

        // Create JWT
        const token = jwt.sign({ sub: email }, SECRET_KEY, { expiresIn: '7d' });

        return res.status(200).json({
            access_token: token,
            token_type: 'bearer',
            user: {
                id: user.id,
                email: user.email,
                username: user.username,
                is_premium: user.is_premium
            }
        });

    } catch (error) {
        console.error('Login error:', error);
        return res.status(500).json({ detail: error.message });
    }
};
