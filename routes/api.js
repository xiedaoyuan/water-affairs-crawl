const express = require('express');
const router = express.Router();
const { Pool } = require('pg');

// 数据库连接池配置
const pool = new Pool({
    user: process.env.DB_USER,
    host: process.env.DB_HOST,
    database: process.env.DB_NAME,
    password: process.env.DB_PASSWORD,
    port: process.env.DB_PORT,
});

// 搜索接口
router.post('/search', async (req, res) => {
    const keyword = req.body.keyword || '';
    try {
        const result = await pool.query(
            'SELECT title, location, time, link FROM waterwater WHERE title ILIKE $1 OR location ILIKE $1',
            [`%${keyword}%`]
        );
        res.json(result.rows);
    } catch (error) {
        console.error('Database error:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

module.exports = router;