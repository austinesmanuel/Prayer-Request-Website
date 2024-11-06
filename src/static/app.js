const socket = io();

function incrementPrayer(prayerId) {
    fetch('/increment_counter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: prayerId })
    });
}

function submitPrayerRequest() {
    const text = document.getElementById('prayer-text').value;
    fetch('/add_prayer_request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    }).then(() => {
        document.getElementById('prayer-text').value = '';
    });
}

socket.on('update_counter', function(data) {
    const prayer = document.querySelector(`.prayer-item[data-id="${data.id}"] .counter`);
    if (prayer) prayer.textContent = data.counter;
});

socket.on('new_prayer', function(data) {
    const prayerList = document.getElementById('prayer-list');
    const newPrayer = document.createElement('div');
    newPrayer.className = 'prayer-item';
    newPrayer.setAttribute('data-id', data.id);
    newPrayer.innerHTML = `<p>${data.text}</p><button onclick="incrementPrayer(${data.id})">Pray</button><p>Prayed: <span class="counter">0</span> times</p>`;
    prayerList.appendChild(newPrayer);
});
