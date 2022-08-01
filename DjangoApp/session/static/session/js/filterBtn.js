const btn = document.getElementById('filterBtn');

btn.addEventListener('click', () => {
  const form = document.getElementById('filterForm');
  // Toggle Display of Form
  if (form.style.display === 'none') {
    form.style.display = '';
  } else {
    form.style.display = 'none';
  }
});