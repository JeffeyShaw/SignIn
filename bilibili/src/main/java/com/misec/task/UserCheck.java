package com.misec.task;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.oldwu.log.OldwuLog;
import lombok.extern.log4j.Log4j2;
import com.misec.apiquery.ApiList;
import com.misec.pojo.userinfobean.Data;
import com.misec.utils.HelpUtil;
import com.misec.utils.HttpUtils;

import static com.misec.task.TaskInfoHolder.STATUS_CODE_STR;
import static com.misec.task.TaskInfoHolder.userInfo;

/**
 * 登录检查
 *
 * @author @JunzhouLiu @Kurenai
 * @since 2020-11-22 4:57
 */
@Log4j2
public class UserCheck implements Task {

    @Override
    public void run() {
        JsonObject userJson = HttpUtils.doGet(ApiList.LOGIN);
        if (userJson == null) {
            OldwuLog.warning("用户信息请求失败，如果是412错误，请在config.json中更换UA，412问题仅影响用户信息确认，不影响任务");
            log.info("用户信息请求失败，如果是412错误，请在config.json中更换UA，412问题仅影响用户信息确认，不影响任务");
        } else {
            userJson = HttpUtils.doGet(ApiList.LOGIN);
            //判断Cookies是否有效
            if (userJson.get(STATUS_CODE_STR).getAsInt() == 0
                    && userJson.get("data").getAsJsonObject().get("isLogin").getAsBoolean()) {
                userInfo = new Gson().fromJson(userJson
                        .getAsJsonObject("data"), Data.class);
                OldwuLog.log("Cookies有效，登录成功");
                log.info("Cookies有效，登录成功");
            } else {
                OldwuLog.error(String.valueOf(userJson));
                log.debug(String.valueOf(userJson));
                OldwuLog.error("Cookies可能失效了,请仔细检查配置中的DEDEUSERID SESSDATA BILI_JCT三项的值是否正确、过期");
                log.warn("Cookies可能失效了,请仔细检查配置中的DEDEUSERID SESSDATA BILI_JCT三项的值是否正确、过期");

                return;
            }
            OldwuLog.log("硬币余额: " + userInfo.getMoney());
            OldwuLog.log("用户名称: " + HelpUtil.userNameEncode(userInfo.getUname()));
            log.info("用户名称: {}", HelpUtil.userNameEncode(userInfo.getUname()));
            log.info("硬币余额: {}", userInfo.getMoney());
        }
    }

    @Override
    public String getName() {
        return "登录检查";
    }
}
