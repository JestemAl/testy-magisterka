const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function runPerformanceTest(url, testName) {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  let tracingStarted = false;

  try {
    await page.goto(url);
    await page.waitForSelector('body', { timeout: 60000 });

    const resultsDir = path.join(__dirname, 'results');
    if (!fs.existsSync(resultsDir)) {
      fs.mkdirSync(resultsDir, { recursive: true });
    }

    const tracePath = path.join(resultsDir, `${testName}-trace.json`);
    const resultPath = path.join(resultsDir, `${testName}-performance-results.txt`);

    await page.tracing.start({ path: tracePath, screenshots: true });
    tracingStarted = true;

    const startTime = Date.now();
    const duration = 2 * 60 * 1000;
    const interval = 1000;
    const results = [];

    console.log(`Starting performance test for ${testName} at ${new Date().toISOString()}`);

    const captureMetrics = async () => {
      try {
        const metrics = await page.metrics();
        const performanceTiming = await page.evaluate(() => JSON.stringify(window.performance.timing));
        const memoryUsage = await page.evaluate(() => JSON.stringify(window.performance.memory));
        const modelCount = await page.evaluate(() => {
          const customStats = document.getElementById('customStats');
          return customStats ? customStats.innerText.split('\n')[0].split(': ')[1] : 0;
        });
        const fps = await page.evaluate(() => {
          const customStats = document.getElementById('customStats');
          return customStats ? parseInt(customStats.innerText.split('\n')[1].split(': ')[1], 10) : 0;
        });

        results.push({
          timestamp: new Date().toISOString(),
          metrics,
          performanceTiming: JSON.parse(performanceTiming),
          memoryUsage: JSON.parse(memoryUsage),
          modelCount,
          fps
        });

        console.log(`Captured metrics at ${new Date().toISOString()}`);
      } catch (error) {
        console.error(`Error capturing metrics: ${error}`);
      }
    };

    const intervalId = setInterval(captureMetrics, interval);

    setTimeout(async () => {
      clearInterval(intervalId);

      if (tracingStarted) {
        await page.tracing.stop();
      }
      await browser.close();

      const endTime = Date.now();
      console.log(`Finished performance test for ${testName} at ${new Date().toISOString()}`);
      console.log(`Total test duration: ${(endTime - startTime) / 1000} seconds`);

      const resultText = `Performance Test Results for ${testName}:\n\n` +
        results.map(result => (
          `Timestamp: ${result.timestamp}\n` +
          `Metrics: ${JSON.stringify(result.metrics, null, 2)}\n` +
          `Performance Timing: ${JSON.stringify(result.performanceTiming, null, 2)}\n` +
          `Memory Usage: ${JSON.stringify(result.memoryUsage, null, 2)}\n` +
          `Number of Models: ${result.modelCount}\n` +
          `FPS: ${result.fps}\n`
        )).join('\n\n');

      fs.writeFileSync(resultPath, resultText);
      console.log(`Performance results saved to ${resultPath}`);
    }, duration);

  } catch (error) {
    console.error(`Error during performance test for ${testName}:`, error);

    if (tracingStarted) {
      await page.tracing.stop();
    }

    const errorLogPath = path.join(__dirname, 'results', `${testName}-error.log`);
    fs.writeFileSync(errorLogPath, `Error during performance test for ${testName}:\n${error.stack}`);
    console.log(`Error details saved to ${errorLogPath}`);
  }
}

async function main() {
  const url = 'http://localhost:5173/';
  const testName = 'webgpu-baked';

  console.log(`Running ${testName} performance test...`);
  await runPerformanceTest(url, testName);
}

main();
