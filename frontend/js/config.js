const CONFIG = {
    API_URL: 'http://localhost:8000',
    WS_URL: 'ws://localhost:8000'
};

if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
