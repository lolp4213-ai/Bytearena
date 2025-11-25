function getCookie(name){
  var v = document.cookie.match('(^|;)\s*' + name + '\s*=\s*([^;]+)');
  return v ? decodeURIComponent(v.pop()) : null;
}

function addToBasket(gameId, title, image, description){
  let basket = JSON.parse(localStorage.getItem('basket') || '[]');
  let item = basket.find(x => x.id === gameId);
  if(item){
    item.count++;
  } else {
    basket.push({id: gameId, title, image, description, count: 1});
  }

  localStorage.setItem('basket', JSON.stringify(basket));
  loadBasket();
}

function removeFromBasket(gameId){
  let basket = JSON.parse(localStorage.getItem('basket') || '[]');
  basket = basket.filter(x => x.id !== gameId);
  localStorage.setItem('basket', JSON.stringify(basket));
  loadBasket();
}

function loadBasket(){
  const basketDiv = document.getElementById('basket-list');
  if(!basketDiv) return;
  
  let basket = JSON.parse(localStorage.getItem('basket') || '[]');
  
  if(basket.length === 0){
    basketDiv.innerHTML = '<p>Корзина порожня.</p>';
    return;
  }

  basketDiv.innerHTML = '';
  basket.forEach(item => {
    const div = document.createElement('div');
    div.className = 'block';
      div.innerHTML = `
        <img src="${item.image || '/img/game1.jpg'}" alt="${item.title}" style="width:80px;height:80px;vertical-align:middle;margin-right:12px;">
        <span style="font-size:18px;">${item.title}</span>
        <p>${item.description || ''}</p>
        <p>Кількість: ${item.count}</p>
      `;
      const buyBtn = document.createElement('button');
      buyBtn.textContent = 'Купити';
      buyBtn.onclick = () => alert('Покупка: ' + item.title);
      buyBtn.style.marginRight = '8px';
      const removeBtn = document.createElement('button');
      removeBtn.textContent = 'Видалити';
      removeBtn.onclick = () => removeFromBasket(item.id);
      div.appendChild(buyBtn);
      div.appendChild(removeBtn);
      basketDiv.appendChild(div);
  });
}

document.addEventListener('DOMContentLoaded', function(){
  if(document.getElementById('basket-list')){
    loadBasket();
  }
});
