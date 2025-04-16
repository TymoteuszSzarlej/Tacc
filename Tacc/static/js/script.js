
// Przykładowy efekt futurystycznego kliknięcia
document.querySelectorAll('.btn').forEach(btn => {
btn.addEventListener('click', () => {
btn.classList.add('pulse');
setTimeout(() => btn.classList.remove('pulse'), 300);
});
});

