import {test,expect} from '@playwright/test';
test('dashboard, navigation and analyst management',async({page})=>{
 const errors:string[]=[];page.on('pageerror',error=>errors.push(error.message));
 await page.goto('/');
 await expect(page.getByRole('heading',{name:'Daily command centre'})).toBeVisible();
 await expect(page.getByText('Fictional teams, players and fixtures. Excluded from real performance.')).toBeVisible();
 await expect(page.getByText('Example City Comets').first()).toBeVisible();
 await page.getByRole('button',{name:'Analysts',exact:true}).click();
 await expect(page.getByText('Exclusive Analytics', {exact:true})).toBeVisible();
 const name=`Browser test analyst ${Date.now()}`;
 await page.getByLabel('Display name').fill(name);
 await page.getByRole('button',{name:'Save',exact:true}).click();
 await expect(page.getByText('Saved successfully')).toBeVisible();
 await expect(page.getByRole('cell',{name,exact:true})).toBeVisible();
 await page.getByRole('button',{name:'Predictions',exact:true}).click();
 await expect(page.getByRole('heading',{name:'Record and lock prediction'})).toBeVisible();
 await page.getByRole('button',{name:'Paper portfolio',exact:true}).click();
 await expect(page.getByRole('heading',{name:'Virtual paper ledger'})).toBeVisible();
 await page.getByRole('button',{name:'Data centre',exact:true}).click();
 await page.getByLabel('CSV content (see README for columns)').fill('name,abbreviation\nBrowser Team,BRT');
 await page.getByLabel('Source reference').fill('Synthetic browser test');
 await page.getByRole('button',{name:'Validate / import'}).click();
 await expect(page.locator('pre')).toContainText('"committed": false');
 await expect(page.locator('pre')).toContainText('"valid_rows": 1');
 await page.getByRole('button',{name:'Learning centre',exact:true}).click();
 await expect(page.getByRole('heading',{name:'Learn through the project'})).toBeVisible();
 expect(errors).toEqual([]);
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBeTruthy();
});

test('create and lock a synthetic selection then record paper units',async({page,request})=>{
 // Create isolated synthetic metadata so repeats never modify the seeded examples.
 const suffix=Date.now().toString(36);
 async function post(path:string,body:unknown){const res=await request.post('/api/v1/'+path,{data:body});expect(res.ok()).toBeTruthy();return res.json()}
 const home=await post('teams',{name:'Browser Home '+suffix,abbreviation:'H'+suffix.slice(-6),synthetic:true});
 const away=await post('teams',{name:'Browser Away '+suffix,abbreviation:'A'+suffix.slice(-6),synthetic:true});
 const player=await post('players',{name:'Browser Player '+suffix,team_id:home.id,synthetic:true});
 const game=await post('games',{season:'DEMO',start_utc:new Date(Date.now()+86400000).toISOString(),home_team_id:home.id,away_team_id:away.id,source:'Synthetic browser fixture',synthetic:true});
 await page.goto('/');await page.getByRole('button',{name:'Predictions',exact:true}).click();
 await page.getByRole('combobox',{name:'Analyst',exact:true}).selectOption('demo-analyst');
 await page.getByRole('combobox',{name:'Fixture',exact:true}).selectOption(game.id);
 await page.getByRole('combobox',{name:'Player',exact:true}).selectOption(player.id);
 await page.getByLabel('Threshold',{exact:true}).fill('10.5');
 await page.getByLabel('Recorded decimal odds (optional)').fill('1.9');
 await page.getByLabel('Overtime rule').selectOption('yes');
 await page.getByLabel('Verified market rule reference').fill('Synthetic standard rules');
 await page.getByLabel('Evidence source').fill('Synthetic browser selection');
 await page.getByRole('button',{name:'Lock prediction'}).click();
 await expect(page.getByText('Saved successfully')).toBeVisible();
 await expect(page.getByRole('cell').filter({hasText:'Browser Player '+suffix})).toBeVisible();
 await page.getByRole('button',{name:'Paper portfolio',exact:true}).click();
 const single=page.getByLabel('Single (choose one target)');
 const options=await single.locator('option').all();let id='';
 for(const option of options)if((await option.textContent())?.includes('Browser Player '+suffix))id=(await option.getAttribute('value'))||'';
 expect(id).toBeTruthy();await single.selectOption(id);
 const form=page.getByRole('heading',{name:'Record virtual paper units'}).locator('..');
 await form.getByRole('button',{name:'Save',exact:true}).click();
 await expect(form.getByText('Saved successfully')).toBeVisible();
});
