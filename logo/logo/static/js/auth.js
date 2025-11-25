(function(){
  function getCookie(name){
    var v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return v ? decodeURIComponent(v.pop()) : null;
  }

  function showUserInNav(username){
    var navRegister = document.getElementById('nav-register');
    var navLogin = document.getElementById('nav-login');
    var userArea = document.getElementById('user-area');
    if(userArea){
      userArea.style.display = 'inline-block';
      var link = document.getElementById('user-link');
      if(link){ link.textContent = username; link.href = '/'; }
    }
    if(navRegister) navRegister.style.display = 'none';
    if(navLogin) navLogin.style.display = 'none';
    var addLink = document.getElementById('add-game-link');
    if(addLink) addLink.style.display = 'inline-block';
  }

  function clearUserInNav(){
    var navRegister = document.getElementById('nav-register');
    var navLogin = document.getElementById('nav-login');
    var userArea = document.getElementById('user-area');
    if(userArea) userArea.style.display = 'none';
    if(navRegister) navRegister.style.display = 'inline-block';
    if(navLogin) navLogin.style.display = 'inline-block';
    var addLink = document.getElementById('add-game-link');
    if(addLink) addLink.style.display = 'none';
  }

  document.addEventListener('DOMContentLoaded', function(){
    var user = getCookie('user');
    if(user){
      showUserInNav(user);
    } else {
      clearUserInNav();
    }
  });
})();
