import {defineConfig} from '@playwright/test';
export default defineConfig({testDir:'e2e',workers:1,use:{baseURL:'http://127.0.0.1:8000',launchOptions:{executablePath:process.env.CHROMIUM_PATH,args:['--no-sandbox']}},projects:[{name:'desktop',use:{viewport:{width:1440,height:1000}}},{name:'mobile',use:{viewport:{width:390,height:844}}}]});
