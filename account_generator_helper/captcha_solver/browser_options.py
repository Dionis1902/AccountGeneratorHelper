from selenium import webdriver

options_array = ['--cryptauth-http-host ""',
                 '--disable-accelerated-2d-canvas',
                 '--disable-background-networking',
                 '--disable-background-timer-throttling',
                 '--disable-browser-side-navigation',
                 '--disable-client-side-phishing-detection',
                 '--disable-default-apps',
                 '--disable-dev-shm-usage',
                 '--disable-device-discovery-notifications',
                 '--disable-extensions',
                 '--disable-features=site-per-process',
                 '--disable-hang-monitor',
                 '--disable-java',
                 '--disable-popup-blocking',
                 '--disable-prompt-on-repost',
                 '--disable-setuid-sandbox',
                 '--disable-sync',
                 '--disable-translate',
                 '--disable-web-security',
                 '--disable-webgl',
                 '--metrics-recording-only',
                 '--no-first-run',
                 '--safebrowsing-disable-auto-update',
                 '--no-sandbox',
                 '--enable-automation',
                 '--password-store=basic',
                 '--use-mock-keychain',
                 '--window-size=360,600',
                 '--window-position=000,000',
                 '--disable-features=IsolateOrigins',
                 '--disable-site-isolation-trials']

options = webdriver.ChromeOptions()
for option in options_array:
    options.add_argument(option)
