const btn1 = document.getElementById('playedTuneGroupAddFormBtn');
const btn2 = document.getElementById('hidePlayedTuneGroupAddFormBtn');

btn1.addEventListener('click', () => {
  const form = document.getElementById('playedTuneGroupAddForm');
  // Toggle Display of Form
  if (form.style.display === 'none') {
    form.style.display = '';
  } else {
    form.style.display = 'none';
  }
  // Toggle Display of Filter Btn
  if (btn1.style.display === 'none') {
    btn1.style.display = '';
  } else {
    btn1.style.display = 'none';
  }
});

btn2.addEventListener('click', () => {
  const form = document.getElementById('playedTuneGroupAddForm');
  // Toggle Display of Form
  if (form.style.display === 'none') {
    form.style.display = '';
  } else {
    form.style.display = 'none';
  }
  // Toggle Display of Filter Btn
  if (btn1.style.display === 'none') {
    btn1.style.display = '';
  } else {
    btn1.style.display = 'none';
  }
});