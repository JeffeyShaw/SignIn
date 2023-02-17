// 参考定时任务:	55 0 */3 * * *	
// 每3个小时运行一次，一天运行8次
//需要在青龙添加node依赖juejin-helper 例如：pnpm install juejin-helper 或 在青龙页面依赖中添加 juejin-helper
const JuejinHelper = require('juejin-helper');
//调用青龙通知文件
const file = require('path').join(__dirname, `sendNotify.js`);
const notify = require(file)
//let ck = JSON.parse(process.env.juejin)
let ck={
  "法外狂徒张三":"复制粘贴替换cookie到这里",
  // "篮球恶霸某鲲":"复制粘贴替换cookie到这里",
}

let command = [];
const commandkey = ["R", "U", "L", "D"];
const cradNum = 3; //上下左右卡片数量 （一般每局四种各有3块 如果四种都不止3块可以改这里）
const cradArr = cradNum * 4; //路线长度 默认用完4种块
var resp={};
var msg=[];
// var isend=0;
function NumbersOccur(val) {
    var newArrays = command.filter(function (item) {
        return item == val;
    });
    return newArrays.length < cradNum ? true : false;
};

//随机生成游戏路线防卡步
function randomCommand() {
    command=[]
    for (let i = 0; command.length < cradArr; i++) {
        let val = commandkey[Math.floor(Math.random() * 4)];
        if (NumbersOccur(val)) {
            command.push(val);
        }
    }
}
async function jueJinGames(e) {
    const juejin = new JuejinHelper();
    await juejin.login(ck[e.user_id]);
    const seagold = juejin.seagold();
    let growth = juejin.growth();
    let LotteryConfig=await growth.getLotteryConfig();
    if (LotteryConfig.free_count>0) {
        let val=await growth.drawLottery();
    }
    var todayDiamond=0
    let steps=50;//运行50次后退出,防止一直循环请求
    let count=0; //记录循环次数

	var results = await new Promise(function (resolve,reject) {
        // query(strSql,function (err,datas) {
                // if (err) {
                    // reject("{ 'success': 0, 'error':"+err.message +"}");
                // } else if (datas.length == 0) {
                    // reject("{ 'success': 0, 'error':'没有找到要修改的数据'}");
                // }
                // resolve(datas);
            // })  
		
		let signTime = setInterval(async () => {
			if(todayDiamond==0){
				randomCommand()
			}
			try {
				await seagold.gameLogin(); // 登陆游戏
				let gameInfo = null;
				const info = await seagold.gameInfo(); // 游戏状态
				if (info.gameStatus === 1) {
					gameInfo = info.gameInfo; // 继续游戏
				} else {
					gameInfo = await seagold.gameStart(); // 开始游戏
				}
				await seagold.gameCommand(gameInfo.gameId, command); // 执行命令
				const result = await seagold.gameOver(); // 游戏结束
				todayDiamond=result.gameDiamond
				//console.log(`${e.user_id}:本次游戏结束获得${result.gameDiamond}矿石,今日上限${result.todayLimitDiamond},今日以获取${result.todayDiamond} ${result.todayDiamond == result.todayLimitDiamond ? '今日获取已达上限运行结束' : '等待下一次运行'}`); // => { ... }
				count++; //计数器+1
				let dd =`${e.user_id}:本次获得${result.gameDiamond}矿石,今日上限${result.todayLimitDiamond},今日获取${result.todayDiamond} ${result.todayDiamond == result.todayLimitDiamond ? "已上限运行结束":"等待下一次运行"}`;
				console.log(dd);
				if (result.todayDiamond == result.todayLimitDiamond||count>=steps){
					resp[e.user_id] = await growth.getCurrentPoint();
					// myPrint(dd);
					myPrint('共循环了'+count+'次');
					myPrint(`今日游戏获得: ${result.todayDiamond}矿石 ， 剩余矿石 ${ resp[e.user_id]}。`)
					// msg+=dd;
					// msg+= `编号:${e.user_id} 今日游戏获得: ${result.todayDiamond}矿石 ， 剩余矿石 ${ resp[e.user_id]}。\n`
					// msg+='共循环了'+count+'次';
					// isend++;
					// if(isend>=Object.keys(ck).length) notify.sendNotify(`掘金签到完成`, msg)
					clearInterval(signTime)
					juejin.logout();
					resolve();
				}
			} catch (error) {
				let reg= new RegExp(/不足/g)
				if(reg.test(error.message)){
				const result = await seagold.gameOver(); // 游戏结束
				}
				resolve()
			}
		}, 12000)
	});
}
async function auto(e) {
    myPrint(`开始执行:${e.user_id}`)
    // console.log(`开始执行:${e.user_id}`)
    const juejin = new JuejinHelper();
    await juejin.login(ck[e.user_id]);
    var growth = juejin.growth();
    try {
        let res = await growth.checkIn() //签到
        resp[e.user_id] = await growth.getCurrentPoint();
        myPrint(`签到成功!剩余矿石${resp[e.user_id]}`);
        // console.log(`签到成功!剩余矿石${resp[e.user_id]}`);
        await juejin.logout();
    } catch (error) {
        resp[e.user_id]= await growth.getCurrentPoint();
        myPrint(`${error.message},当前剩余${resp[e.user_id]}个矿石`)
        // let msg = [error.message, `当前剩余${resp[e.user_id]}个矿石`] 
        // console.log(msg);
        await juejin.logout();
    }
}
async function LuckyDraw(e) {
    const juejin = new JuejinHelper();
    await juejin.login(ck[e.user_id]);
    const growth = juejin.growth();
    let res=await growth.getLotteryConfig();
    if (res.free_count>0) {
        let val=await growth.drawLottery();
        myPrint(val);
        // console.log(val);
    }
    
}

async function bugfix(e) {
  const juejin = new JuejinHelper();
  await juejin.login(ck[e.user_id]);
  const growth = juejin.growth();
  await growth.getLotteryConfig();
  const bugfix = juejin.bugfix();
  const notCollectBugList = await bugfix.getNotCollectBugList();
  await bugfix.collectBugBatch(notCollectBugList);
  const competition = await bugfix.getCompetition();
  const bugfixInfo = await bugfix.getUser(competition);
  myPrint(`收集Bug ${notCollectBugList.length}个,未消除Bug数量 ${bugfixInfo.user_own_bug}个`);
  // let print=`key:${e.user_id} 收集Bug ${notCollectBugList.length}个,未消除Bug数量 ${bugfixInfo.user_own_bug}个\n`
  //msg +=print
  // isend++
  // console.log(print,isend)
  // if(isend>=Object.keys(ck).length) {
    // notify.sendNotify(`Bug拾取完成`, msg)
  // }
  await juejin.logout();
}


function myPrint(txt){
	console.log(txt);
	msg.push(txt);
}

async function mian(){
myPrint('共有个'+Object.keys(ck).length+'账号')
      for(const key in ck){
		myPrint('--------------')
        await auto({ user_id: key })
        await jueJinGames({ user_id: key })
        await LuckyDraw({ user_id: key })
        await bugfix({ user_id: key })
      }
	  notify.sendNotify(`稀土掘金`, msg.join('\n'))
}
mian()

