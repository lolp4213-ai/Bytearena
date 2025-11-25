document.addEventListener('DOMContentLoaded', function(){
  const container = document.getElementById('games-list');
  if(!container) return;
  fetch('/api/games').then(r=>r.json()).then(games=>{
    if(!games || games.length===0){
      container.innerHTML = '<p>No games yet. Be the first to add one!</p>';
      return;
    }
    container.innerHTML = '';
    games.forEach(g=>{
      const div = document.createElement('div');
      div.className = 'block';
      const img = document.createElement('img');
      img.src = g.image || '/img/game1.jpg';
      img.alt = g.title;
      const span = document.createElement('span');
      span.textContent = g.title;
      const p = document.createElement('p');
      p.textContent = g.description || '';
      const owner = document.createElement('small');
      owner.style.display = 'block';
      owner.style.color = '#ddd';
      owner.textContent = g.owner ? ('Added by ' + g.owner) : '';
      div.appendChild(img);
      div.appendChild(span);
      div.appendChild(p);
      div.appendChild(owner);
      // Add to basket button
      const btn = document.createElement('button');
      btn.textContent = 'Add to basket';
      btn.onclick = function(){ 
        addToBasket(g.id, g.title, g.image, g.description);
        animateBasket(img);
      };
      div.appendChild(btn);
      // Link to basket page
      const basketLink = document.createElement('a');
      basketLink.href = '/basket';
      basketLink.textContent = 'Go to basket';
      basketLink.className = 'basket-link';
      div.appendChild(basketLink);
      container.appendChild(div);

      // Animation function
      function animateBasket(imgElem){
        const basketDiv = document.getElementById('basket-list');
        if(!basketDiv || !imgElem) return;
        const clone = imgElem.cloneNode(true);
        const rect = imgElem.getBoundingClientRect();
        clone.style.position = 'fixed';
        clone.style.left = rect.left + 'px';
        clone.style.top = rect.top + 'px';
        clone.style.width = rect.width + 'px';
        clone.style.zIndex = 9999;
        clone.style.transition = 'all 0.7s cubic-bezier(.4,2,.3,1)';
        document.body.appendChild(clone);
        setTimeout(()=>{
          const basketRect = basketDiv.getBoundingClientRect();
          clone.style.left = basketRect.left + 'px';
          clone.style.top = basketRect.top + 'px';
          clone.style.width = '32px';
          clone.style.opacity = '0.2';
        }, 50);
        setTimeout(()=>{
          document.body.removeChild(clone);
        }, 800);
      }
    })
  }).catch(err=>{
    container.innerHTML = '<p>Failed to load games.</p>';
    console.error(err);
  });
});
