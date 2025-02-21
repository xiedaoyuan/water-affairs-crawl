document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const keyword = document.querySelector('.search-box').value.trim();
    if (!keyword) return;

    // 发送AJAX请求
    fetch('/api/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ keyword }),
    })
    .then(response => response.json())
    .then(data => {
        const resultsDiv = document.getElementById('search-results');
        resultsDiv.innerHTML = '';

        if (data.length === 0) {
            resultsDiv.innerHTML = '<p>未找到相关结果。</p>';
            return;
        }

        // 动态生成HTML内容
        const resultsHTML = data.map(item => `
            <div class="result-item">
                <h3>${item.title}</h3>
                <p>位置：${item.location}</p>
                <p>日期：${item.time}</p>
                <a href="${item.link}" target="_blank">查看原文</a>
            </div>
        `).join('');

        resultsDiv.innerHTML = resultsHTML;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('搜索失败，请稍试后再。');
    });
});