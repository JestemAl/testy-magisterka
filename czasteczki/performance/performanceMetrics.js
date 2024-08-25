import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';

async function runPerformanceTest(url, testName) {
    const browser = await puppeteer.launch({
        headless: false,
        executablePath: 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
    });
    const page = await browser.newPage();

    await page.setViewport({ width: 1920, height: 1080 });

    const startLoadTime = Date.now();
    await page.goto(url);
    await page.waitForSelector('canvas.webgl', { timeout: 60000 });
    const loadTime = Date.now() - startLoadTime;

    const resultsDir = path.join(path.resolve(), 'results');
    if (!fs.existsSync(resultsDir)) {
        fs.mkdirSync(resultsDir, { recursive: true });
    }

    const resultPath = path.join(resultsDir, `${testName}-performance-results.txt`);
    fs.writeFileSync(resultPath, `Czas ładowania (Load Time): ${loadTime} ms\n`);

    const duration = 0.5 * 60 * 1000; // 5 minut
    const interval = 1000; // 1 sekunda
    const warmUpTime = 10000; // 10 sekund

    console.log(`Starting performance test for ${testName} at ${new Date().toISOString()}`);

    const captureMetrics = async () => {
        try {
            const metrics = await page.evaluate(() => {
                return {
                    fps: window.statsData.fps,
                    avgCpuTime: window.statsData.cpu,
                    avgGpuTime: window.statsData.gpu,
                    avgFrameTime: window.renderInfo.totalFrameTime,
                    drawCalls: window.renderInfo.drawCalls,
                };
            });

            if (metrics) {
                const resultText = `FPS: ${metrics.fps}\n` +
                                   `GPU Frame Time: ${metrics.avgGpuTime} ms\n` +
                                   `CPU Frame Time: ${metrics.avgCpuTime} ms\n` +
                                   `Draw Calls: ${metrics.drawCalls}\n` +
                                   `Total Frame Time: ${metrics.avgFrameTime} ms\n\n`;

                console.log('Appending results to file...');
                fs.appendFileSync(resultPath, resultText);
            } else {
                console.log('Metrics are null or empty, skipping...');
            }
        } catch (error) {
            console.error(`Error capturing metrics: ${error}`);
        }
    };

    setTimeout(() => {
        console.log('Warm-up complete, starting metrics capture...');
        const intervalId = setInterval(captureMetrics, interval);

        setTimeout(async () => {
            clearInterval(intervalId);
            await browser.close();
            console.log(`Finished performance test for ${testName} at ${new Date().toISOString()}`);
        }, duration);
    }, warmUpTime);
}

async function main() {
    const url = 'http://localhost:5173/';
    const browser = await puppeteer.launch({
        headless: false,
        executablePath: 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
    });
    // const page = await browser.newPage();

    // await page.goto(url);
    // const seedValue = await page.evaluate(() => window.seedNumber);

    const testName = `czasteczki-seed`;

    console.log(`Running ${testName} performance test...`);
    await runPerformanceTest(url, testName);

    await browser.close();
}

main();
