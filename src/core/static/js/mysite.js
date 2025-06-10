
window.addEventListener('scroll', (ev) => {
  const scrollTop = document.body.scrollTop || document.documentElement.scrollTop;
  document.body.classList.toggle('scrolled', scrollTop > 300);
});
