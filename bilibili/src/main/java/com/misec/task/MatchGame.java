package com.misec.task;


import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.misec.apiquery.ApiList;
import com.misec.apiquery.OftenApi;
import com.misec.config.ConfigLoader;
import com.misec.login.Verify;
import com.misec.utils.HttpUtils;
import com.misec.utils.SleepTime;
import com.oldwu.log.OldwuLog;
import lombok.extern.log4j.Log4j2;

import java.net.URLEncoder;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * @author junzhou
 */
@Log4j2
public class MatchGame implements Task {

    @Override
    public void run() {
        if (!ConfigLoader.getTaskConfig().getMatchGame()) {
            log.info("赛事预测未开启");
            OldwuLog.log("赛事预测未开启");
            return;
        }
        double currentCoin = OftenApi.getCoinBalance();

        if (currentCoin < ConfigLoader.getTaskConfig().getMinimumNumberOfCoins()) {
            OldwuLog.log(ConfigLoader.getTaskConfig().getMinimumNumberOfCoins() + "个硬币都没有，参加你\uD83D\uDC34预测呢？任务结束");
            log.info("{}个硬币都没有，参加什么预测呢？任务结束", ConfigLoader.getTaskConfig().getMinimumNumberOfCoins());
            return;
        }
        JsonObject resultJson = queryContestQuestion(getTime(), 1, 50);
        JsonObject jsonObject = resultJson.get("data").getAsJsonObject();
        if (resultJson.get("code").getAsInt() == 0) {
            JsonArray list = jsonObject.get("list").getAsJsonArray();
            JsonObject pageinfo = jsonObject.get("page").getAsJsonObject();
            if (pageinfo.get("total").getAsInt() == 0) {
                log.info("今日无赛事或者本日赛事已经截止预测");
                OldwuLog.log("今日无赛事或者本日赛事已经截止预测");
                return;
            }
            if (list != null) {
                int coinNumber = ConfigLoader.getTaskConfig().getPredictNumberOfCoins();
                int contestId;
                String contestName;
                int questionId;
                String questionTitle;
                int teamId;
                String teamName;
                //   int seasonId;
                String seasonName;
                for (JsonElement listinfo : list) {
                    log.info("-----预测开始-----");
                    OldwuLog.log("-----预测开始-----");
                    if (currentCoin < ConfigLoader.getTaskConfig().getMinimumNumberOfCoins()) {
                        log.info("仅剩{}个硬币，低于最低保留硬币数量，后续预测不再执行", currentCoin);
                        OldwuLog.log("仅剩{" + currentCoin + "}个硬币，低于最低保留硬币数量，后续预测不再执行");
                        break;
                    }
                    JsonObject contestJson = listinfo.getAsJsonObject().getAsJsonObject("contest");
                    JsonObject questionJson = listinfo.getAsJsonObject().getAsJsonArray("questions").get(0).getAsJsonObject();
                    contestId = contestJson.get("id").getAsInt();
                    contestName = contestJson.get("game_stage").getAsString();
                    questionId = questionJson.get("id").getAsInt();
                    questionTitle = questionJson.get("title").getAsString();
                    //seasonId = contestJson.get("season").getAsJsonObject().get("id").getAsInt();
                    seasonName = contestJson.get("season").getAsJsonObject().get("title").getAsString();
                    OldwuLog.log(seasonName + " " + contestName + ":" + questionTitle);
                    log.info("{} {}:{}", seasonName, contestName, questionTitle);

                    if (questionJson.get("is_guess").getAsInt() == 1) {
                        log.info("此问题已经参与过预测了，无需再次预测");
                        OldwuLog.log("此问题已经参与过预测了，无需再次预测");
                        continue;
                    }
                    JsonObject teamA = questionJson.get("details").getAsJsonArray().get(0).getAsJsonObject();
                    JsonObject teamB = questionJson.get("details").getAsJsonArray().get(1).getAsJsonObject();
                    log.info("当前赔率为:  {}:{}", teamA.get("odds").getAsDouble(), teamB.get("odds").getAsDouble());
                    OldwuLog.log("当前赔率为:  " + teamA.get("odds").getAsDouble() + ":" + teamB.get("odds").getAsDouble());

                    if (ConfigLoader.getTaskConfig().getShowHandModel()) {
                        if (teamA.get("odds").getAsDouble() <= teamB.get("odds").getAsDouble()) {
                            teamId = teamB.get("detail_id").getAsInt();
                            teamName = teamB.get("option").getAsString();
                        } else {
                            teamId = teamA.get("detail_id").getAsInt();
                            teamName = teamA.get("option").getAsString();
                        }
                    } else {
                        if (teamA.get("odds").getAsDouble() >= teamB.get("odds").getAsDouble()) {
                            teamId = teamB.get("detail_id").getAsInt();
                            teamName = teamB.get("option").getAsString();
                        } else {
                            teamId = teamA.get("detail_id").getAsInt();
                            teamName = teamA.get("option").getAsString();
                        }
                    }
                    log.info("拟预测的队伍是:{},预测硬币数为:{}", teamName, coinNumber);
                    OldwuLog.log("拟预测的队伍是:" + teamName + ",预测硬币数为:" + coinNumber);
                    currentCoin -= coinNumber;
                    doPrediction(contestId, questionId, teamId, coinNumber);
                    new SleepTime().sleepDefault();
                }
            }
        } else {
            log.info("获取赛事信息失败");
            OldwuLog.error("获取赛事信息失败");
        }
    }

    private JsonObject queryContestQuestion(String today, int pn, int ps) {
        String gid = "";
        String sids = "";
        String urlParam = "";
        try {
            urlParam = "?pn=" + pn
                    + "&ps=" + ps
                    + "&gid=" + gid
                    + "&sids=" + sids
                    + "&stime=" + today + URLEncoder.encode(" 00:00:00", "UTF-8")
                    + "&etime=" + today + URLEncoder.encode(" 23:59:59", "UTF-8");
        } catch (Exception ignored) {

        }
        return HttpUtils.doGet(ApiList.QUERY_QUESTIONS + urlParam);
    }

    private void doPrediction(int oid, int main_id, int detail_id, int count) {
        String requestbody = "oid=" + oid
                + "&main_id=" + main_id
                + "&detail_id=" + detail_id
                + "&count=" + count
                + "&is_fav=0"
                + "&csrf=" + Verify.getInstance().getBiliJct();

        JsonObject result = HttpUtils.doPost(ApiList.DO_MATCH_ADD, requestbody);

        if (result.get("code").getAsInt() != 0) {
            log.info(result.get("message").getAsString());
            OldwuLog.log(result.get("message").getAsString());
        } else {
            log.info("预测成功");
            OldwuLog.log("预测成功");
        }

    }

    private String getTime() {
        Date d = new Date();
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        return sdf.format(d);
    }

    @Override
    public String getName() {
        return "赛事预测";
    }
}
