document.addEventListener('DOMContentLoaded', function() {
    const btcDiv = document.getElementById('btc-div')
    const satoshiDiv = document.getElementById('satoshi-div')
    const usdDiv = document.getElementById('usd-div')

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