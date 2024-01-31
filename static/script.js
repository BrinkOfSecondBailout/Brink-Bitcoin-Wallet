document.addEventListener('DOMContentLoaded', function() {
    const btcDiv = document.getElementById('btc-div')
    const satoshiDiv = document.getElementById('satoshi-div')
    const usdDiv = document.getElementById('usd-div')

    const receiveDiv = document.getElementById('receive-div');
    receiveDiv.style.display = 'none';
    const sendDiv = document.getElementById('send-div');
    sendDiv.style.display = 'none';
    const withdrawDiv = document.getElementById('withdraw-div');
    withdrawDiv.style.display = 'none';

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
    const sendButton = document.getElementById('send-button');
    const sendDiv = document.getElementById('send-div');
    const withdrawButton = document.getElementById('withdraw-button');
    const withdrawDiv = document.getElementById('withdraw-div');

    if(receiveDiv.style.display === 'none') {
        receiveDiv.style.display = 'flex';
        receiveButton.classList.add('active-button');
        sendDiv.style.display = 'none';
        sendButton.classList.remove('active-button');
        withdrawDiv.style.display = 'none';
        withdrawButton.classList.remove('active-button');
    } else {
        receiveDiv.style.display = 'none';
        receiveButton.classList.remove('active-button');
    }
}

function sendBitcoin(e) {
    e.preventDefault();
    const sendButton = document.getElementById('send-button');
    const sendDiv = document.getElementById('send-div');
    const receiveDiv = document.getElementById('receive-div');
    const receiveButton = document.getElementById('receive-button');
    const withdrawButton = document.getElementById('withdraw-button');
    const withdrawDiv = document.getElementById('withdraw-div');

    if(sendDiv.style.display === 'none') {
        sendDiv.style.display = 'flex';
        sendButton.classList.add('active-button');
        receiveDiv.style.display = 'none';
        receiveButton.classList.remove('active-button');
        withdrawDiv.style.display = 'none';
        withdrawButton.classList.remove('active-button');
    } else {
        sendDiv.style.display = 'none';
        sendButton.classList.remove('active-button');
    }
}

function withdrawBitcoin(e) {
    e.preventDefault();
    const withdrawButton = document.getElementById('withdraw-button');
    const withdrawDiv = document.getElementById('withdraw-div');
    const receiveButton = document.getElementById('receive-button');
    const receiveDiv = document.getElementById('receive-div');
    const sendButton = document.getElementById('send-button');
    const sendDiv = document.getElementById('send-div');

    if(withdrawDiv.style.display === 'none') {
        withdrawDiv.style.display = 'flex';
        withdrawButton.classList.add('active-button');
        receiveDiv.style.display = 'none';
        receiveButton.classList.remove('active-button');
        sendDiv.style.display = 'none';
        sendButton.classList.remove('active-button');
    } else {
        withdrawDiv.style.display = 'none';
        withdrawButton.classList.remove('active-button');
    }

}