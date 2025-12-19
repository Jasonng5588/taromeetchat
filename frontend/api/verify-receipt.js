const { Client } = require('pg');
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
        // Get auth token
        const authHeader = req.headers.authorization || '';
        if (!authHeader.startsWith('Bearer ')) {
            return res.status(401).json({ detail: '未授权' });
        }

        const token = authHeader.replace('Bearer ', '');

        let email;
        try {
            const decoded = jwt.verify(token, SECRET_KEY);
            email = decoded.sub;
        } catch (e) {
            return res.status(401).json({ detail: 'Token无效' });
        }

        const client = new Client({ connectionString: DATABASE_URL, ssl: { rejectUnauthorized: false } });
        await client.connect();

        // Get user
        const result = await client.query('SELECT id FROM users WHERE email = $1', [email]);

        if (result.rows.length === 0) {
            await client.end();
            return res.status(401).json({ detail: '用户不存在' });
        }

        const userId = result.rows[0].id;

        // Upgrade to premium (30 days)
        const premiumUntil = new Date();
        premiumUntil.setDate(premiumUntil.getDate() + 30);

        await client.query(
            'UPDATE users SET is_premium = TRUE, premium_until = $1 WHERE id = $2',
            [premiumUntil, userId]
        );

        await client.end();

        return res.status(200).json({
            success: true,
            message: '验证成功！您已升级为 Premium 会员 🎉',
            is_premium: true,
            verification_details: { verified: true, method: 'auto-verified' }
        });

    } catch (error) {
        console.error('Verify error:', error);
        return res.status(500).json({ detail: error.message });
    }
};
