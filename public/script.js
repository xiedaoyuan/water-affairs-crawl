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
        if (data.length === 0) {
            document.getElementById('search-results').innerHTML = '<p>未找到相关结果。</p>';
            return;
        }
        displayResults(data); // 使用displayResults函数处理结果
    })
    .catch(error => {
        console.error('Error:', error);
        alert('搜索失败，请稍试后再。');
    });
});

let currentPage = 1;
const itemsPerPage = 50;
let allResults = []; // 用于存储所有搜索结果

function displayResults(results) {
    allResults = results; // 保存所有结果
    updateDisplay();
}

function updateDisplay() {
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedResults = allResults.slice(startIndex, endIndex);
    
    const resultsContainer = document.getElementById('search-results');
    resultsContainer.innerHTML = '';
    
    // 添加结果显示逻辑
    const resultsHTML = paginatedResults.map(item => `
        <div class="result-item">
            <h3>${item.title}</h3>
            <p>位置：${item.location}</p>
            <p>日期：${item.time}</p>
            <a href="${item.link}" target="_blank">查看原文</a>
        </div>
    `).join('');
    
    resultsContainer.innerHTML = resultsHTML;
    
    updatePagination();
}

function updatePagination() {
    const totalPages = Math.ceil(allResults.length / itemsPerPage);
    document.getElementById('current-page').textContent = currentPage;
    document.getElementById('total-pages').textContent = totalPages; // 添加总页数显示
    
    const prevBtn = document.querySelector('.page-btn:first-child');
    const nextBtn = document.querySelector('.page-btn:last-child');
    prevBtn.disabled = currentPage === 1;
    nextBtn.disabled = currentPage === totalPages;
}

function jumpToPage() {
    const pageInput = document.getElementById('page-input');
    const pageNumber = parseInt(pageInput.value);
    const totalPages = Math.ceil(allResults.length / itemsPerPage);
    
    if (isNaN(pageNumber) || pageNumber < 1 || pageNumber > totalPages) {
        alert(`请输入有效的页码（1-${totalPages}）`);
        return;
    }
    
    currentPage = pageNumber;
    updateDisplay();
}

function nextPage() {
    currentPage++;
    updateDisplay();
}

function prevPage() {
    currentPage--;
    updateDisplay();
}

// 在你的搜索函数中调用displayResults