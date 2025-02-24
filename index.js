const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
require('dotenv').config();

// 创建 express 应用实例
const app = express();
// 设置端口号，优先使用环境变量中的 PORT，如果没有则使用 3000
const port = process.env.PORT || 3000;

// 中间件配置
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));

// 引入路由模块
const apiRoutes = require('./routes/api');
// 使用 '/api' 路径前缀应用 apiRoutes
app.use('/api', apiRoutes);

// 启动服务器
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});