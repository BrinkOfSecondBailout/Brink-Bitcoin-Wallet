document.addEventListener('DOMContentLoaded', function() {
    const btcDiv = document.getElementById('btc-div')
    const satoshiDiv = document.getElementById('satoshi-div')
    const usdDiv = document.getElementById('usd-div')

    const receiveDiv = document.getElementById('receive-div');
    receiveDiv.style.display = 'none';

    satoshiDiv.style.display = 'none';
    usdDiv.style.display = 'none';

    const switchIcon = document.getElementById('switch-icon');

    switchIcon.addEventListener('click', function() {
        if (btcDiv.style.display !== 'none') {
            btcDiv.style.display = 'none';
            satoshiDiv.style.display = 'flex';
        } else if (satoshiDiv.style.display !== 'none') {
            satoshiDiv.style.display = 'none';
            usdDiv.style.display = 'flex';
        } else {
            usdDiv.style.display = 'none';
            btcDiv.style.display = 'flex';
        }
    });
});

function receiveBitcoin(e) {
    e.preventDefault();
    const receiveButton = document.getElementById('receive-button');
    const receiveDiv = document.getElementById('receive-div');

    if(receiveDiv.style.display === 'none') {
        receiveDiv.style.display = 'flex';
        receiveButton.classList.add('active-button');
    } else {
        receiveDiv.style.display = 'none';
        receiveButton.classList.remove('active-button');
    }
}