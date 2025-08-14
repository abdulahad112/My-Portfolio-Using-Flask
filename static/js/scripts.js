// Animate skill bars when loaded
function animateSkillBars(){
  document.querySelectorAll('.skill-bar').forEach(bar=>{
    const pct = bar.getAttribute('data-pct') || 0;
    const inner = bar.querySelector('.progress-bar');
    inner.style.width = pct + '%';
    inner.setAttribute('aria-valuenow', pct);
  });
}

const themeToggle = document.getElementById('themeToggle');
function setTheme(t){
  if(t === 'light') document.documentElement.setAttribute('data-theme','light');
  else document.documentElement.removeAttribute('data-theme');
  localStorage.setItem('theme', t);
}

themeToggle && themeToggle.addEventListener('click', ()=>{
  const cur = localStorage.getItem('theme') || 'dark';
  setTheme(cur === 'dark' ? 'light' : 'dark');
});

document.addEventListener('DOMContentLoaded', ()=>{
  const saved = localStorage.getItem('theme') || 'dark';
  setTheme(saved);
  animateSkillBars();
});
